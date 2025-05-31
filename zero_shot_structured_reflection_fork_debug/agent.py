from error import InvalidOpenAIFinishReasonError, FailedOpenAIRequestError
from openai import OpenAI
from anthropic import Anthropic
from config import GLOBAL_CONFIG
import json
import time

class APIUsageManager:
    usage = {}
    response_time = {}

    @classmethod
    def record_usage(cls, module, model, usage):
        if module not in cls.usage:
            cls.usage[module] = {
                'model': model,
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0,
            }
        cls.usage[module]['prompt_tokens'] += usage.prompt_tokens
        cls.usage[module]['completion_tokens'] += usage.completion_tokens
        cls.usage[module]['total_tokens'] += usage.total_tokens

    @classmethod
    def record_response_time(cls, model, response_time):
        if model not in cls.response_time:
            cls.response_time[model] = []
        cls.response_time[model].append(response_time)

    @classmethod
    def get_usage(cls):
        return cls.usage
    
    @classmethod
    def get_response_time(cls):
        return cls.response_time
    
    @classmethod
    def reset(cls):
        cls.usage = {}
        cls.response_time = {}

class Agent:
  def ask(prompt, client= "anthropic", model=None, temperature = 0, max_tokens = 2048, module = "all", json_response=False):
    model = model if model else GLOBAL_CONFIG['agent']['model']
    response = None
    if client == "openai":
      client = OpenAI(api_key = GLOBAL_CONFIG['agent']['key'])
      try:
        if json_response:
          response = client.chat.completions.create(
            model= model,
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={ 'type': 'json_object' },
            seed=0
          )
        else:
          response = client.chat.completions.create(
            model= model,
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
          )
      except Exception as e:
        raise FailedOpenAIRequestError(e)
      
      if (response.choices[0].finish_reason != "stop" and response.choices[0].finish_reason != "length"):
        raise InvalidOpenAIFinishReasonError()
      
      APIUsageManager.record_usage(module, model, response.usage)
      if (json_response):
        return json.loads(response.choices[0].message.content)
      else:
        return response.choices[0].message.content
    elif client == "anthropic":
      client = Anthropic(api_key = GLOBAL_CONFIG['agent']['key'])
      try:
        if json_response:
          response = client.messages.create(
            max_tokens=1000,
            model= model,
            temperature=temperature,
            system=prompt[0]["content"],
            messages=[
                prompt[1]
            ],
          )
      except Exception as e:
        raise FailedOpenAIRequestError(e)
      # print(response.content[0].text)
      
      if (json_response):
        return json.loads(response.content[0].text)
      else:
        return response.content[0].text
    elif client == "llama":
      pass