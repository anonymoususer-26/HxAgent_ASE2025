from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from error import CannotPerformActionError
from abc import abstractmethod
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Action:
    def __init__(self, xpath, description = None, description_detail = None):
        self.xpath = xpath
        self.description = description
        self.description_detail = description_detail

    @abstractmethod
    def _perform(self, driver):
        pass

    @abstractmethod
    def _toSeleniumScript(self):
        pass

    def perform(self, driver):
        try:
            is_flight_task = None
            try:
                wrap_element = driver.find_element(By.ID, "wrap")
                if (wrap_element.tag_name == "iframe"):
                    driver.switch_to.frame(driver.find_element(By.ID, "wrap"))
                    driver.get_lis_html()
                    is_flight_task = True
            except NoSuchElementException:
                pass
            self._perform(driver)
            if (is_flight_task):
                driver.switch_to.default_content()
        except Exception as e:
            if (is_flight_task):
                driver.switch_to.default_content()
            raise CannotPerformActionError(e, self.xpath)

    def toSeleniumScript(self):
        return self._toSeleniumScript()
    
    def __str__(self):
        return self.description


class ClickAction(Action):
    def __init__(self, xpath, description = "Click"):
        super().__init__(xpath)
        self.description = description

    def _perform(self, driver):
        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable((By.XPATH, self.xpath))).click()
    
    def _toSeleniumScript(self):
        return f"wait.until(EC.element_to_be_clickable((By.XPATH, '{self.xpath}'))).click()"

class InputAction(Action):
    def __init__(self, xpath, content, description = "Input"):
        super().__init__(xpath, description)
        self.content = content

    def _perform(self, driver):
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        element.clear()
        element.send_keys(self.content)
    
    def _toSeleniumScript(self):
        return f"""element = wait.until(EC.presence_of_element_located((By.XPATH, '{self.xpath}')))
element.clear()
element.send_keys('{self.content}')"""
    
class WaitAction(Action):
    def __init__(self, seconds, description = "Wait"):
        super().__init__(None, description)
        self.seconds = seconds

    def _perform(self, driver):
        sleep(self.seconds)

    def _toSeleniumScript(self):
        return f"driver.implicitly_wait({self.seconds})"
    
class EnterAction(Action):
    def __init__(self, xpath, description = "Enter"):
        super().__init__(None, description)
        self.xpath = xpath

    def _perform(self, driver):
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        element.send_keys(Keys.RETURN)

    def _toSeleniumScript(self):
        return f"element.send_keys(Keys.RETURN)"
    
class ChainAction(Action):
    def __init__(self, actions, description = "Form submit"):
        super().__init__("chain_action_xpath", description)
        self.actions = actions

    def _perform(self, driver):
        for action in self.actions:
            action.perform(driver)
    
    def _toSeleniumScript(self):
        script = ""
        for action in self.actions:
            script += action.toSeleniumScript() + "\n"
        return script