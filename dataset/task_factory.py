from selenium.webdriver.common.by import By
from abc import abstractmethod
import random
import re

class Factory:    
    @abstractmethod
    def create(self, simulator):
        pass

class TaskFactory:
    def __init__(self, id: str, url: str, title: str, task_template: str, *args):
        self.id = id
        self.url = url
        self.title = title
        self.task_template = task_template
        self.args = args
        self.randomized = False
        self.iterative = [0 for _ in range(len(args))]
    
    def create(self, simulator=None):
        if (self.randomized):
            instance = [arg[random.randint(0, len(arg)-1)] for arg in self.args]
        else:
            instance = [arg[self.iterative[idx] % len(arg)] for idx, arg in enumerate(self.args)]
            self.iterative = [i+1 for i in self.iterative]
        return self.task_template.format(*instance)

class MiniwobTaskFatory(TaskFactory):
    def __init__(self, id: str, url: str, title: str):
        self.id = id
        self.url = url
        self.title = title
        self.seed = 0
        self.randomized = False

    def create(self, simulator):
        if (self.randomized):
            self.seed = random.randint(0, 100000)
        else:
            self.seed += 1 
        with open('./dataset/miniwob/core/core.js') as f:
            code = f.read()
        code = re.sub(r"Math.seedrandom(.+);", f"Math.seedrandom('{str(self.seed)}');", code, flags=re.MULTILINE)
        with open('./dataset/miniwob/core/core.js', 'w') as f:
            f.write(code)
        simulator.init(self.url)
        return simulator.find_element(By.ID, "query").text