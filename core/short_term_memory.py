from core.utils import remove_whitespace
from core.simulator import Simulator
from core.action import Action
from core.state import State
from pathlib import Path

class ShortTermMemory:
    def __init__(self, url: str, title: str, task: str = None, size: int = -1):
        self.url = url
        self.task = task
        self.title = title
        self.trail = []
        self.failed_reason = None
        self.size = size
    
    def append(self, action: Action, state: State):
        self.trail.append({ "action": action, "state": state })

    def stringify(self) -> str:
        serialized_trail = ""
        start_index = 0
        if (self.size != -1):
            start_index = max(0, len(self.trail)-self.size)
        for i in range(start_index, len(self.trail)):
            serialized_trail += f"""> STATE #{i+1}: {str(self.trail[i]['state'].description)}
> STEP #{i+1}: {str(self.trail[i]['action'].description)}\n"""
        memory_str = f"""You are visiting the website title: {self.title}
You are asked to complete the following task: {self.task} \n
You have completed the following steps:\n{serialized_trail if serialized_trail != "" else "No steps taken, you are at the starting screen"}""".strip()
        return memory_str

    def stringify_short(self) -> str:
        serialized_trail = ""
        for i in range(len(self.trail)):
            if self.trail[i]['action'].description == "Wait":
                continue
            serialized_trail += f"""> STATE #{i+1}: {str(self.trail[i]['state'].description)}
> STEP #{i+1}: {str(self.trail[i]['action'].description)}\n"""
        memory_str = f"""Task: {self.task} \n
{serialized_trail if serialized_trail != "" else "No steps taken, you are at the starting screen"}""".strip()
        if (self.failed_reason):
            memory_str += f"\nFailed reason: {self.failed_reason}"
        return memory_str 

    def lis_stringify(self) -> str:
        if (len(self.trail) == 0):
            return "No steps taken, you are at the starting screen"
        serialized_trail = ""
        for i in range(len(self.trail)):
            serialized_trail += f"""STEP #{i+1}: {str(self.trail[i]['action'].description_detail)}"""
            if (i != len(self.trail)-1):
                serialized_trail += "\n"
        return serialized_trail

    def lis_stringify_details(self) -> str:
        if (len(self.trail) == 0):
            return "No steps taken, you are at the starting screen"
        serialized_trail = ""
        for i in range(len(self.trail)):
            serialized_trail += f"""The index={i+1} screen: {self.trail[i]['state'].description}
The index={i+1} action: {self.trail[i]['action'].description}\n"""
            if (i != len(self.trail)-1):
                serialized_trail += "\n"
        return serialized_trail
    
    def save_script(self, path: str, simulator: Simulator):
        path = Path(remove_whitespace(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            script = simulator.toSetupScript()
            script += "\n"
            for pair in self.trail:
                script += pair['action'].toSeleniumScript() + "\n"
            f.write(script)

    def to_script(self, simulator: Simulator):
        script = simulator.toSetupScript()
        script += "\n"
        for pair in self.trail:
            script += pair['action'].toSeleniumScript() + "\n"
        return script

    