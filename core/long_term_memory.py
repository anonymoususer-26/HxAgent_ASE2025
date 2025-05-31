from core.agent_access import AgentAccess
from core.short_term_memory import ShortTermMemory
from core.utils import serialize
from config import GLOBAL_CONFIG

class LongTermMemory:
    def __init__(self):
        self.successful_trials = []
        self.failed_trials = []
        self.rules = []

    def update(self, short_term_memory: ShortTermMemory, is_success: bool, failed_reason: str = ""):
        if is_success:
            self.successful_trials.append(short_term_memory)
        else:
            short_term_memory.failed_reason = failed_reason
            self.failed_trials.append(short_term_memory)
            self._try_extract_rule()
                
    def _try_extract_rule(self):
        rules = self.rules[-GLOBAL_CONFIG['long_term_memory']['rule']['max']:]
        serialized_successful_trials = serialize([trial.stringify_short() for trial in self.successful_trials], "SUCCESSFUL TRIAL") if self.successful_trials else "No successful trial found."
        serialized_failed_trials = serialize([trial.stringify_short() for trial in self.failed_trials], "FAILED TRIAL") if self.failed_trials else "No failed trial found."
        new_rule = AgentAccess.extract_rule(serialized_successful_trials, serialized_failed_trials, rules)
        if new_rule:
            self.rules.append(new_rule)

    def stringify(self):
        serialized_successful_trials = serialize([trial.stringify_short() for trial in self.successful_trials], "SUCCESSFUL TRIAL") if self.successful_trials else "No successful trial found."
        rules = self.rules[-GLOBAL_CONFIG['long_term_memory']['rule']['max']:]
        serialized_rules = serialize(rules, "RULE") if self.rules else ""
        memory_str = f'{"# Here are the history of your trials" if serialized_successful_trials else ""}' + "\n" + serialized_successful_trials + "\n" + serialized_rules
        return memory_str.strip()