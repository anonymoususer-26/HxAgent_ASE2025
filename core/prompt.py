SYSTEM_CONTENT_GENERATE = """
I want you to act as input content generator for a new website application.
You will need to generate the input for the given input field to satisfy the task/requirements.
You are given the following information:
# Information 1: A task that you need to complete in the website.
Example: "Forward email of user Alice to user Bob"

# Information 2: The steps you have taken so far to complete the task.
Example:
STEP #1: Click on the Email thread of user Alice

# Information 3: The given input field is described in following JSON format:
{
"tagName": This field indicates the type of HTML element the input field belongs to (e.g., "input" for an input field),
"attributes": This field provides additional attributes associated with the input field, such as ID, class, name, etc. It could be represented as a JSON object containing key-value pairs of attributes and their respective values,
"text": This field represents the visible text content within the input field, if applicable. For input fields, this might typically be empty unless it's a pre-filled input,
"belongTo": This field provides contextual parent information of the element (optional). This can be used to help you understand the context of the element.
}

# Information 4: The previous success trials as well as the rules extracted from past trials to help you generate the input content.

Do not include any personal opinions or subjective evaluations in your description.
IMPORTANT:
1. If the page context is given, you should consider the context to generate the input.
2. You should first analyze the function of the input field, then extract the necessary information from the requirement/task and/or the page context to generate the input content.
The format of the JSON response must strictly follow this rules:
1. Output the response in a JSON formated like:
{
"description": a detail description of the step you do, eg. <operation> <content> on <element>
"content": the content to input as string; if the input should be kept unchanged or does not relevant to the input content, return 0
}
For example:
{
"description": "Input "admin" to the Username field",
"content": "admin"   
}

IMPORTANT: You must only output the JSON response without any additional information.
"""

SYSTEM_TASK_CLARIFY = """I want you to act as a website assistant that helps users understand the task better by providing a detailed explanation of the task.
You will be given the current task and the current state of the website. Your job is to describe and clarify the task.
The format of the JSON response must strictly follow this rules:
{
"clarified_task": ... (a string describe the task after clarification)
}
If the task has date time, it would be in MM/DD/YYYY format, please clarifies it as follows
Example: "date 5/8/2022" will be clarified as "the date (day=8, month=5, year=2022)"

You must not omit any information provided in the original task. Only make it clearer and more understandable. Please do not change the input content information in the task (if any).
"""

SYSTEM_CHOOSE_ACTION_PROMPT = """
You are a web assistant designed to help users navigate a website and complete tasks. As an AI-powered agent, you can learn from our history trials to improve decision-making and better assist me over time.
You will complete the task by taking a series of steps. Each step is a description of the action you take and the specific item, entity, or element on the website that the action is applied to. 
Drawing from history trials on why you SUCCESS, you need to chose the most potential of the next step to solve the task based on the past steps you have taken.
You also need to update your policy based on learned RULES from past attempts to choose the most potential of the next step better and maximize the success rate over time.

You will be given the following information:
# Information 1: A task that you need to complete in the website.
Example: "Forward email of user Alice to user Bob"

# Information 2: The steps you have taken so far to complete the task.
Example:
STEP #1: Click on the Email thread of user Alice
STEP #2: Click on the Forward button

# Information 3: A list of possible next steps you can take
Example:
POSSIBLE NEXT STEP #1: 
{
  "operation": "click"
  "target object": {
    "attributes": {"id": "send-button"},
    "text: "Send",
    "belongTo": ...contextual parent information of the element (optional), this can be used to help you to understand the context of the element
  }
}

POSSIBLE NEXT STEP #2:
{
  "operation": "input",
  "target object": {
    "attributes": {"id": "recipient-email"},
    "text: "",
    "belongTo": ...contextual parent information of the element (optional), this can be used to help you to understand the context of the element
  }
}

Your job is to choose the most possible next steps to help you complete the task.
Do not include any personal opinions or subjective evaluations in your response.

# The format of the response must strictly follow this JSON format:
{
"chosen_action": ... (the index of the potential action that you choose, start from #1)
}

IMPORTANT: If there is a dropdown item after inputting the autocomplete field, you should consider selecting the most relevant item.
IMPORTANT: You must only output the JSON response without any additional information.
"""


SYSTEM_CHOOSE_ACTION_VISION_PROMPT = """
You are a web assistant designed to help users navigate a website and complete tasks. As an AI-powered agent, you can learn from our history trials to improve decision-making and better assist me over time.
You will complete the task by taking a series of steps. Each step is a description of the action you take and the specific item, entity, or element on the website that the action is applied to. 
Drawing from history trials on why you SUCCESS, you need to chose the most potential of the next step to solve the task based on the past steps you have taken.
You also need to update your policy based on learned RULES from past attempts to choose the most potential of the next step better and maximize the success rate over time.

You will be given the following information:
# Information 1: A task that you need to complete in the website.
Example: "Forward email of user Alice to user Bob"

# Information 2: The steps you have taken so far to complete the task.
Example:
STEP #1: Click on the Email thread of user Alice
STEP #2: Click on the Forward button

# Information 3: An image of the current state of the website that contains the highlighted possible next actions you can take along with its index.

Your job is to choose the most possible next actions to help you complete the task.
Do not include any personal opinions or subjective evaluations in your response.

# The format of the response must strictly follow this JSON format:
{
"chosen_action": ... (the index of the potential action that you choose)
}

IMPORTANT: You must only output the JSON response without any additional information.
"""

SYSTEM_DESCRIBE_STATE = """
Act as a human navigate through the web, analyze the given DOM content and provide necessary information to solve the given task.
Output the response in a JSON formated like:
{
  "summary_prev": Summary of my previous interactions for the task <1~2 sentences according to the task execution history and web state. Be careful not to include any actions that haven't been performed yet>
  "description": Description of the current state <2~3 sentences, describe the current web state according to the hierarchical structure I provided>
}

IMPORTANT: You must only output the JSON response without any additional information.
IMPORTANT: If there is a date time in the task, it would be in MM/DD/YYYY format, please describe it as follows: "the date (day=8, month=5, year=2022)"
IMPORTANT: Be careful for dropdown after inputting the input field, you should describe the dropdown item in the description as follow: "There is an dropdown item with the text '...' after inputting the ... to ...."
"""

SYSTEM_DESCRIBE_STATE_VISION = """
Act as a human navigate through the web, analyze the given web screenshot and provide necessary information to solve the given task.
Output the response in a JSON formated like:
{
  "summary_prev": Summary of my previous interactions for the task <1~2 sentences according to the task execution history and web state. Be careful not to include any actions that haven't been performed yet>
  "description": Description of the current state <2~3 sentences, describe the current web state according to the web screenshot I provided>
  "early_stop": Decide whether to stop the task early due to significant divergence from the expected state. <1 for early stop, 0 for continue>
  "is_done": Decide whether the task is completed based on previous steps and current state. <1 for done, 0 for not done>
}
IMPORTANT: You must only output the JSON response without any additional information.
IMPORTANT: If there is a date time in the task, it would be in MM/DD/YYYY format, please describe it as follows: "the date (day=8, month=5, year=2022)"
IMPORTANT: Be careful for dropdown after inputting the input field, you should describe the dropdown item in the description as follow: "There is an dropdown item with the text '...' after inputting the ... to ...."
"""

SYSTEM_TERMINATION_PROMPT = """
I want you to act as a judge for an automated system that solves simple tasks in web environment.

You will be given the following information:
# Information 1: A task that you need to complete in the website.
Example: "Forward email of user Alice to user Bob"

# Information 2: The steps you have taken so far to complete the task along with the web state description for each step
Example:
STATE #1: ...
STEP #1: Click on the Email thread of user Alice

STATE #2: ...
STEP #2: Click on the Forward button

You need to decide if the steps form a complete plan to solve the task.
Output the response in a JSON formated like:
{
  "done": 1 if the steps are enough to complete the task, 0 if there is still work need to be done to complete the task
}

An example output for the above task might be:
{
  "done": 0
}
The steps are not enought as it lasks the step where the user need to input the name "Bob" into the forwarding field.

IMPORTANT: You must only output the JSON response without any additional information.
"""

SYSTEM_RULE_EXTRACTION = """I want you to act as an evaluator in the Reinforcement Learning system to obtain the set of rules from trials and errors to train the policy model.
You will be given the history of a past experience in which you were placed in a web environment and given a task to complete. You were both success and unsuccessful in completing the task. Do not summarize your environment, but rather compare the strategy and path you took to attempt to complete the task in both cases. Devise a concise rule that accounts for your mistake in the given task to apply it to evaluate for the step in the future trials on similar task on whether the step is good or bad.
The format of the JSON response must strictly follow this rules:
{
"rule": ... (a string describe the rule) or 0 if the rules extracted from past attempts already sufficient
}
IMPORTANT: Do not repeat the rule from past attempts when generating new rule. If you have extracted all the rules, just return "No rule left".
IMPORTANT: Please describe the rule detail with definition and example to help the system understand the rule better.
IMPORTANT: Keep the rule in 2-3 sentences length maximum.
IMPORTANT: You must only output the JSON response without any additional information.
"""


SYSTEM_GEN_PLAN_PROMPT = """
You are a web assistant designed to help users navigate a website and complete tasks.
You will complete the task by devising a plan.

You will be given the following information:
# Information 1: A task that you need to complete in the website.
Example: "Forward email of user Alice to user Bob"

# Information 2: A list of possible steps in the starting page
Example:
POSSIBLE NEXT STEP #1: 
{
  "action description": "Click on the Send button"
  "target object": {
    "tagName": "button",
    "attributes": {"id": "send-button"},
    "text: "Send",
    "belongTo": ...contextual parent information of the element (optional), this can be used to help you to understand the context of the element
  }
}

POSSIBLE NEXT STEP #2:
{
  "action description": "Input "Bob" into the recipient field",
  "target object": {
    "tagName": "input",
    "attributes": {"id": "recipient-email"},
    "text: "",
    "belongTo": ...contextual parent information of the element (optional), this can be used to help you to understand the context of the element
  }
}

Your job is to devise a complete plan to complete the task
A plan is comprises of many step, each step is a string defined as follow:
<operation> + (<content>) + <element>
where <operation> must be "click" or "input", <element> is the element to operate upon, and <content> is an optional component that is only required
when the <operation> is "input" indicating the content to input.
For example: "Click the send button"
For example: "Input 'alice' into the username field"

You can use imagination to improvise the steps that operate on elements that do not exist in the list provided

A plan is an array of such steps.
# The format of the JSON response must strictly follow this rules:
{
"plan": [] (an array of the steps taken in appropriate order to complete the task)
}
"""

def GenInputContentPrompt(element, history, experience = ""):
  experience = experience if experience else ""
  prompt = experience + """
# Here is the actual task.
{trajectory_memory}
At the next step, you need to generate the input for the below input field to satisfy the requirement/task:
{element}
""".format(trajectory_memory = history, element = element)
  return [
    { "role": "system", "content": SYSTEM_CONTENT_GENERATE },
    { "role": "user", "content": prompt.strip() }
  ]


def ClarifyTaskPrompt(task, dom):
  prompt = f"""The task is: {task}
At the current state, I'll give you the full content of the current page as follows (I organized the page content as a hierarchical structure):
```json
{dom}
```
"""
  return [
      { "role": "system", "content": SYSTEM_TASK_CLARIFY  },
      { "role": "user", "content": prompt.strip() },
  ]

def ChooseActionPrompt(history, state, action, experience = ""):
  experience = experience if experience else ""
  state = state if state else "you reach a new state."
  prompt = experience + f"""# Here is the actual task.
{history}

After completing the above steps, {state}

Now, in this state, the followng possible steps exists:
{action}

Based on the task requirements, previous steps and possible actions, I should select:
""" 
  #+ "{"
  return [
    { "role": "system", "content": SYSTEM_CHOOSE_ACTION_PROMPT },
    { "role": "user", "content": prompt.strip() }
  ]

def ChooseActionVisionPrompt(history, screenshot, experience = ""):
  experience = experience if experience else ""
  prompt = experience + f"""# Here is the actual task.
{history}

After completing the above steps, you reach the following screen:
"""

  return [
    { "role": "system", "content": SYSTEM_CHOOSE_ACTION_VISION_PROMPT },
    { "role": "user", "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": screenshot
            }
          },
    ]
  }
  ]

def DescribeStatePrompt(history, dom):
  prompt = f"""{history}
At the current state, I'll give you the full content of the current page as follows (I organized the page content as a hierarchical structure):
```json
{dom}
```
"""
  return [
    { "role": "system", "content": SYSTEM_DESCRIBE_STATE },
    { "role": "user", "content": prompt.strip() }
  ]

def DescribeStateVisionPrompt(history, screenshot):
  prompt = f"""{history}
At the current state, I'll give you the web screenshot of the current page as follows:

"""
  return [
    { "role": "system", "content": SYSTEM_DESCRIBE_STATE_VISION },
    { "role": "user", "content": [
          {
            "type": "text",
            "text": prompt.strip()
          },
          {
            "type": "image_url",
            "image_url": {
              "url": screenshot
            }
          },
      ]
    } 
  ]
  # This comment code is for claude vision API
  # return [
  #     { "role": "system", "content": SYSTEM_DESCRIBE_STATE_VISION },
  #     { "role": "user", "content": [
  #           {
  #             "type": "text",
  #             "text": prompt.strip()
  #           },
  #           {
  #             "type": "image",
  #             "source": {
  #               "type": "base64", 
  #               "media_type": "image/png",
  #               "data": screenshot
  #             }
  #           },
  #       ]
  #     } 
  #   ]

def TerminationPrompt(history):
  prompt = f"""#Here is the actual task.
{history}
Your decision is:
""" 
  #+ "{"
  return [
    { "role": "system", "content": SYSTEM_TERMINATION_PROMPT },
    { "role": "user", "content": prompt.strip() }
  ]

def ExtractRulePrompt(success, failed, rules):
  prompt = f"""History of the past experience:
# SUCCESS TRIALS:
{success}
# FAILED TRIALS:
{failed}
Rule from past attempts:
{rules}
New rule to extract:
""" 
  #+ "{"
  return [
      { "role": "system", "content": SYSTEM_RULE_EXTRACTION  },
      { "role": "user", "content": prompt.strip() }
  ]

def GenPlanPrompt(task, action):
  prompt = f"""# The task is as follows: {task}

The website contains the following operations:
{action}
"""
  return [
    { "role": "system", "content": SYSTEM_GEN_PLAN_PROMPT },
    { "role": "user", "content": prompt.strip() }
  ]

def LisDescribeActionPrompt(html, action):
  prompt = f"""You are capable of describing actions taken on a computer. The computer screen is represented by the following HTML pseudo code:
<screen> {html} </screen>
And the action taken is: {action}
Now, in plain language, please summarize what has been done. You should describe the specific purpose for the action, instead of simply referring to the element id or position of the element. Summary:"""
  return [
    { "role": "user", "content": prompt }
  ]

def LisPlanActionPrompt(goal, html, trajectory):
  sys_prompt = f"""You can generate a series of atomic actions to fulfill a top-level goal. There are three types of atomic actions you can perform. Firstly, you can click an object by referring to its id, such as "click id=...". Secondly, you can enter text to an input field, such as "enter "..." to id=...".’ Specifically, you should always wrap the text you want to type in with double quotes. You should not wrap the id with double quotes."""
  prompt = f"""The top-level goal: {goal}
You have executed the following actions:
{trajectory}
The computer screen is represented by the following HTML pseudo code:
<screen> {html} </screen>
Now, you need to plan next actions that are executable on and only on this screen. For actions that are not executableon this screen, you should leave them to future planning. Your plan should consist of a list of atomic actions on the screen. Please separate them by newline without adding any indexing."""
  return [
    { "role": "system", "content": sys_prompt },
    { "role": "user", "content": prompt }
  ]

def LisReflectionPrompt(task_name, trajectory, goal, status):
  sys_prompt = f"""There are three types of atomic actions you can perform. Firstly, you can click an object by referring to its id, such as "click id=...". Secondly, you can enter text to an input field, such as "enter "..." to id=...".’ Specifically, you should always wrap the text you want to type in with double quotes. Example output: For action index=2, you should click id=22; For action index=3, you should enter "Alice" to id=33"""
  prompt = f"""You are operating a computer for a task: {task_name}. 
You went over a series of screens and executed actions to fulfill a top-level goal. 
Your action trajectory is as follows:
{trajectory}
You conducted the above actions for the top-level goal: {goal}. {status} Your suggestion should be in this format: "For action index=A, you should B.", where A is the action index, and B is the suggested action you should have taken. Your suggestion:"""
  return [
    { "role": "system", "content": sys_prompt },
    { "role": "user", "content": prompt }
  ]