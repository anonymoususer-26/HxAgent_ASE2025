from core.prompt import GenInputContentPrompt, ClarifyTaskPrompt, ChooseActionPrompt, ChooseActionVisionPrompt, DescribeStatePrompt, DescribeStateVisionPrompt, TerminationPrompt, ExtractRulePrompt, GenPlanPrompt, LisDescribeActionPrompt, LisPlanActionPrompt, LisReflectionPrompt
from core.action import Action, InputAction, ClickAction
from core.utils import serialize, remove_special_characters
from core.agent import Agent
from error import InvalidActionError
import re
import time

class AgentAccess:
    def choose_action(actions: list[Action], state: str, trail: str, experience: str = "", screenshot: str = None) -> tuple[Action, str]:
        serialized_actions = serialize([str(action.description) for action in actions], "POSSIBLE NEXT ACTION")
        if (screenshot != None):
            prompt = ChooseActionVisionPrompt(trail, screenshot, experience)
        else:
            prompt = ChooseActionPrompt(trail, state, serialized_actions, experience)
        agent_response = Agent.ask(prompt, module="agent")
        action = actions[agent_response['chosen_action']-1]
        if (action.description['operation'] == 'input'):
            prompt = GenInputContentPrompt(action.description['target object'], trail, experience)
            agent_input_response = Agent.ask(prompt, module="input_generator")
            action.description['content'] = agent_input_response['content']
            action = InputAction(action.xpath, agent_input_response['content'], action.description)
            if (action.description_detail == None):
                action.description_detail = agent_input_response['description']
        reason = ""
        return action, reason 

    def generate_actions(clickables: list[any], trail: str, experience: str = "") -> list[Action]:
        operations = []
        for clickable in clickables:
            clickable_cp = clickable.copy()
            if ('attributes' in clickable_cp):
                clickable_cp['attributes'].pop('data-event', None)
                clickable_cp['attributes'].pop('data-handler', None)
            if ('style' in clickable_cp):
                clickable_cp.pop('style', None)
            clickable_cp.pop('xpath', None)

            if (clickable["tagName"] in ['input','textarea']):
                if ("checkbox" in str(clickable).lower() or "radio" in str(clickable).lower() or "datepicker" in str(clickable).lower()):
                    clickable_cp.pop('tagName', None)
                    operations.append({ "operation": "click", "element": clickable_cp, "xpath": clickable['xpath']})
                else:
                    clickable_cp.pop('tagName', None)
                    operations.append({ "operation": "input", "element": clickable_cp, "xpath": clickable['xpath']})
            else:
                clickable_cp.pop('tagName', None)
                operations.append({ "operation": "click", "element": clickable_cp, "xpath": clickable['xpath']})
        actions = []
        operation_map = {}
        for idx, operation in enumerate(operations):
            # Check the duplicate elements
            key = remove_special_characters(str(operation["operation"]) + str(operation["element"]))
            if key not in operation_map:
                operation_map[key] = [idx]
            else:
                operation_map[key].append(idx)
            if len(operation_map[key]) > 1:
                if (len(operation_map[key]) == 2):
                    operations[operation_map[key][0]]["element"]["duplicate"] = True
                    operations[operation_map[key][0]]["element"]["duplicate_index"] = 1

                operation["element"]["duplicate"] = True
                operation["element"]["duplicate_index"] = len(operation_map[key])

            if operation['operation'] == 'input':
                description = {
                    "operation": operation["operation"],
                    "target object": operation["element"],
                }
            else:
                description = {
                    "operation": operation["operation"],
                    "target object": operation["element"]
                }
            if (operation['operation'] == 'input'):
                actions.append(InputAction(operation["xpath"], "", description))
            else:
                actions.append(ClickAction(operation["xpath"], description))
        return actions, operation_map

    def clarify_task(dom: str, task: str) -> str:
        prompt = ClarifyTaskPrompt(task, dom)
        agent_response = Agent.ask(prompt, module="clarifier")
        return agent_response['clarified_task']

    def extract_rule(serialized_successful_trials: str, serialized_failed_trials: str, current_rules: list[str]) -> str:
        serialized_current_rules = serialize(current_rules, "RULE") if current_rules else "No current rules found."
        prompt = ExtractRulePrompt(serialized_successful_trials, serialized_failed_trials, serialized_current_rules)
        agent_response = Agent.ask(prompt, module="rule_extractor")
        return agent_response['rule']
    
    def describe_dom_state(trail: str, dom: str) -> str:
        prompt = DescribeStatePrompt(trail, dom)
        agent_response = Agent.ask(prompt, module="content_extractor")
        return agent_response['summary_prev'] + agent_response['description']
    
    def describe_screenshot_state(trail: str, screenshot: str) -> str:
        prompt = DescribeStateVisionPrompt(trail, screenshot)
        agent_response = Agent.ask(prompt, module="content_extractor")
        return agent_response['summary_prev'] + agent_response['description'], agent_response['early_stop'], agent_response['is_done']
    
    def is_done(history: str) -> bool:
        prompt = TerminationPrompt(history)
        agent_response = Agent.ask(prompt, module="terminator")
        return True if agent_response['done'] != 0 else False

    def gen_plan(task: str, actions: list[Action]) -> str:
        serialized_actions = serialize([str(action.description) for action in actions], "ACTION")
        prompt = GenPlanPrompt(task, serialized_actions)
        agent_response = Agent.ask(prompt, module="agent")
        return serialize(agent_response['plan'], "STEP")

    def lis_action_description(html, action):
        prompt = LisDescribeActionPrompt(html, action)
        agent_response = Agent.ask(prompt, json_response=False, module="lis")
        return agent_response

    def __parse_lis_action(action):
        type = action.split(" ")[0]
        if (type == "click"):
            match = re.search(r"id=(\d+)", action)
            if match:
                id = int(match.group(1))
            else:
                id = "notexist"
            return ClickAction(f'//*[@hxagentidentity="{id}"]', action)
        elif (type == "enter"):
            match = re.search(r'"(.*?)"', action)
            if match:
                content = match.group(1)
                match = re.search(r"id=(\d+)", action)
                if match:
                    id = int(match.group(1))
                else:
                    id = "notexist"
                return InputAction(f'//*[@hxagentidentity="{id}"]', content, action)
            else:
                raise InvalidActionError()
        else:
            raise InvalidActionError()
    
    def parse_id_from_lis_actions(actions):
        ids = []
        for action in actions:
            action_description = action.description
            type = action_description.split(" ")[0]
            if (type == "click"):
                match = re.search(r"id=(\d+)", action_description)
                if match:
                    id = int(match.group(1))
                else:
                    id = "notexist"
                ids.append(id)
        return ids

    def lis_staged_plan(goal, html, trajectory):
        prompt = LisPlanActionPrompt(goal, html, trajectory)
        agent_response = Agent.ask(prompt, json_response=False, module="lis")
        actions = agent_response.split("\n")
        parsed_actions = []
        for action in actions:
            if (action == "") or (action == " ") or (action == "\n") or (action == None):
                continue
            parsed_actions.append(AgentAccess.__parse_lis_action(action))
        return parsed_actions
    
    def lis_reflection(task_name, trajectory, goal, status):
        prompt = LisReflectionPrompt(task_name, trajectory, goal, status)
        agent_response = Agent.ask(prompt, json_response=False, module="lis")
        step_id = int(agent_response.split(", you should")[0].split("=")[1].strip()) - 1
        action = agent_response.split(", you should")[1].strip()
        parsed_action = AgentAccess.__parse_lis_action(action)
        return step_id, parsed_action