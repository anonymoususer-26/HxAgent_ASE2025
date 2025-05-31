import re
import json
import time
from rapidfuzz import fuzz

def serialize(array, default_keyword = "STEP"):
    plan = ""
    for i, content in enumerate(array):
        plan += default_keyword + " #" + str(i+1)+': '+str(content)+'\n'
    return plan

def remove_whitespace(content: str) -> str:
    content = content.replace(" ", "")
    content = content.replace("\t", "").replace("\n", "").replace("\r", "")
    content = content.replace('"', '').replace("'", '')
    return content

def remove_special_characters(text):
    # Use regex to remove all characters except alphanumeric and whitespace
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return cleaned_text

def fix_json_string(json_str: str) -> str:
    """
    Fix JSON string by properly escaping quotes in text fields
    """
    # Replace single quotes with double quotes, except for those within text content
    json_str = re.sub(r'(".*?)(\'s|\'\b)(.*?)"', lambda m: m.group(0).replace("'", ""), json_str)
    json_str = json_str.replace("'", '"')
    
    return json_str

def extract_steps(text):
    # Find all STEP entries with their JSON data
    step_pattern = r"> STEP #\d+: ({.*})"
    steps = re.findall(step_pattern, text)
    
    # Convert string representations to actual JSON objects
    steps_json = []
    for step in steps:
        try:
            # Replace single quotes with double quotes for valid JSON
            norm_step = fix_json_string(step)
            step_json = json.loads(norm_step)
            steps_json.append(step_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing step: {e}")
            print(step_json)
            time.sleep(100)
    
    return steps_json

def compare_dict_structure(dict1, dict2) -> float:
    """
    Compare two dictionaries and return a similarity score based on matching keys and values
    """
    score = 0
    total_keys = 0
    
    # Compare common keys and their values
    for key in dict1:
        total_keys += 1
        if key in dict2:
            # If both values are dictionaries, recurse
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                score += compare_dict_structure(dict1[key], dict2[key])
            # If the values are equal, add 1 to score
            elif dict1[key] == dict2[key]:
                score += 1
            # If the values are different but exist, add 0.5 to score
            else:
                #score += 0.5
                score += fuzz.token_set_ratio(dict1[key], dict2[key]) / 100

                
    # Add remaining keys from dict2
    total_keys += len(set(dict2.keys()) - set(dict1.keys()))
    
    return score / total_keys if total_keys > 0 else 0

def find_best_matching_action(step, actions_seq):
    """
    Find the best matching Action type for a given step based on JSON structure
    """
    best_match = None
    highest_score = 0
    
    for action in actions_seq:
        similarity_score = compare_dict_structure(step, action.description)
        if similarity_score > highest_score:
            highest_score = similarity_score
            best_match = action
    
    # You might want to adjust this threshold based on your needs
    SIMILARITY_THRESHOLD = 0.5
    
    return best_match if highest_score >= SIMILARITY_THRESHOLD else None
