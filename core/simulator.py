from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from config import GLOBAL_CONFIG
import difflib
import base64
import time
import json

class Simulator(webdriver.Chrome):
    def __init__(self, force_headless=False):
        self.url = ""
        self.seed = ""
        chrome_options = Options()
        if GLOBAL_CONFIG['simulator']['headless'] or force_headless:
            print("Running in headless mode")
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--lang=en-GB")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument(f"user-data-dir={GLOBAL_CONFIG['simulator']['user_data_dir']}")
        chrome_options.binary_location = GLOBAL_CONFIG['simulator']['binary_location']
        super().__init__(options=chrome_options)

    def restart(self, url=None, seed=None):
        if url:
            self.get(url)
            self.url = url
            self.seed = seed
        else:
            self.get(self.url)
        if ("miniwob" in self.url):
            div_element = self.find_element(By.ID, "sync-task-cover")
            div_element.click()

    def init(self, url):
        self.url = url
        self.get(url)
        if ("miniwob" in self.url):
            div_element = self.find_element(By.ID, "sync-task-cover")
            div_element.click()

    def crawl(self):
        js_file_path = "script/html_extractor.js" 
        with open(js_file_path, "r") as js_file:
            js_script = js_file.read()
        html = self.execute_script(js_script)
        return html
    
    def get_clickables(self):
        js_file_path = ""
        if (".html" in self.url):
            if ("wrapper.html" in self.url):
                js_file_path = "script/miniwob_clickable_extractor_flight.js"
            else:
                js_file_path = "script/miniwob_clickable_extractor.js"
        else:
            js_file_path = "script/clickable_extractor.js" 
        with open(js_file_path, "r") as js_file:
            js_script = js_file.read()
        parameters = {
            "expression": js_script,
            "includeCommandLineAPI": True,
            "returnByValue": True,
        }
        html = self.execute_cdp_cmd("Runtime.evaluate", parameters)
        return html['result']['value']
    
    def get_screenshot_url(self):
        screenshot = self.find_element(By.TAG_NAME, 'body').screenshot_as_png
        data = base64.b64encode(screenshot).decode()
        data_uri = f'data:image/png;base64,{data}'
        return data_uri
    
    def get_screenshot_base64(self):
        screenshot = self.find_element(By.TAG_NAME, 'body').screenshot_as_png
        data = base64.b64encode(screenshot).decode()
        return data
    
    def get_screenshot(self):
        screenshot = self.find_element(By.TAG_NAME, 'body').screenshot_as_png
        return screenshot


    def get_lis_html(self, disable_ids=[]):
        disable_ids_json = json.dumps(disable_ids)
        js_file_path =  "script/li_et_al_extractor.js"
        if ("wrapper.html" in self.url):
            js_file_path = "script/li_et_al_extractor_flight.js"
        with open(js_file_path, "r") as js_file:
            js_script = js_file.read()
        
        js_script = js_script.replace("DISABLE_IDS", disable_ids_json)
        parameters = {
            "expression": js_script,
            "includeCommandLineAPI": True,
            "returnByValue": True,
        }
        html = self.execute_cdp_cmd("Runtime.evaluate", parameters)
        return html['result']['value']
    
    def highlight_element(self, element, idx, duration=2):
        """
        Highlights a Selenium WebDriver element with a bounding box and displays its index.
        
        Parameters:
        - driver: The WebDriver instance.
        - element: The WebElement to highlight.
        - idx: Index of the element (int).
        - duration: How long to highlight the element in seconds.
        """
        script = """
        var element = arguments[0];
        var idx = arguments[1];
        var original_style = element.getAttribute('style');
        element.setAttribute('style', original_style + '; outline: dotted red; outline-offset: -0.2em;');

        
        // Get the element's dimensions
        var rect = element.getBoundingClientRect();

        // Create a label dynamically
        var label = document.createElement('div');
        label.style.position = 'absolute';
        label.style.top = (rect.top - 20) + 'px';  // Position above the element
        label.style.left = (rect.right - rect.width * 0.1) + 'px';  // Adjust relative to element width
        label.style.backgroundColor = 'red';
        label.style.color = 'white';
        label.style.padding = '2px 5px';
        label.style.fontSize = '12px';
        label.style.borderRadius = '3px';
        label.style.zIndex = '1000';
        label.textContent = idx;

        // Attach the label to the document body
        document.body.appendChild(label);
        
        setTimeout(function(){
            element.setAttribute('style', original_style);
            document.body.removeChild(label);
        }, arguments[2] * 1000);
        """
        self.execute_script(script, element, idx, duration)
        
    def has_reach_end(self):
        if "miniwob" in self.url:
            re = self.__get_miniwob_result()
            return re['reward'] != '-'
        return False
    
    def is_successful(self):
        if "miniwob" in self.url:
            re = self.__get_miniwob_result()
            return  float(re['reward'])>= 0
        return None

    def __get_miniwob_result(self):
        js_file_path = "script/miniwob_result_extractor.js" 

        with open(js_file_path, "r") as js_file:
            js_content = js_file.read()

        js_script = f"""
        {js_content}
        """
        re = self.execute_script(js_script)
        return re
    
    def toSetupScript(self):
        if (".html" in self.url):
            return f"""from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import re

# Set up the browser
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)
with open('../../dataset/miniwob/core/core.js') as f:
    code = f.read()
code = re.sub(r"Math.seedrandom(.+);", "Math.seedrandom('{str(self.seed)}');", code, flags=re.MULTILINE)
with open('../../dataset/miniwob/core/core.js', 'w') as f:
    f.write(code)
driver.get("{self.url}")
driver.refresh()
driver.find_element(By.ID, "sync-task-cover").click()

"""
        # TODO: Add support for other types of dataset
        # For real-world datasets, we use the below script
        else:
            return f"""from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 5)

driver.get("{self.url}")

"""