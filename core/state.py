from core.agent_access import AgentAccess
from core.action import Action
from core.utils import serialize

class State:
    def __init__(self, dom: str, interactive_element: list[any], possible_actions: list[Action], screenshot: str = None, describe_option: str = "screenshot"):
        self.dom = dom
        self.interactive_elements = interactive_element
        self.possible_actions = possible_actions
        self.description = None
        self.early_stop = False
        self.is_done = False
        self.describe_option = describe_option
        self.screenshot = screenshot

    def try_describe_state(self, trail: str):
        if self.describe_option == "dom":
            serialized_actions = serialize([str(action.description) for action in self.possible_actions], "POSSIBLE NEXT ACTION")
            self.description = AgentAccess.describe_dom_state(trail, serialized_actions)
        elif self.describe_option == "screenshot":
            self.description, self.early_stop, self.is_done = AgentAccess.describe_screenshot_state(trail, self.screenshot)
        else:
            self.description = None

    def __str__(self) -> str:
        return self.description
    