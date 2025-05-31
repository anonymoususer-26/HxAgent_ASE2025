import traceback

class InvalidOpenAIFinishReasonError(Exception):
  def __init__(self):
    super().__init__("Request to OpenAI does not return 'stop' as finish reason")
    traceback.print_exc()

class FailedOpenAIRequestError(Exception):
  def __init__(self, e):
    super().__init__(f"Request to OpenAI failed {e}")
    traceback.print_exc()

class CannotPerformActionError(Exception):
  def __init__(self, e, xpath):
    super().__init__(f"An action on element failed to execute {e}, xpath = {xpath}")
    traceback.print_exc()
  
class CannotOpenTaskError(Exception):
  def __init__(self):
    super().__init__("Task ID is invalid")
    traceback.print_exc()
    
class InvalidConfiguration(Exception):
  def __init__(self):
    super().__init__("Invalid configuration")
    traceback.print_exc()

class InvalidActionError(Exception):
  def __init__(self):
    super().__init__("Invalid action parse")
    traceback.print_exc()