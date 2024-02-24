from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GameInstance:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
    
    def find_element_by_text(self, text):
        xpath = f"//div[contains(@class, 'item') and contains(text(), '{text}')]"
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element
    
    def drag(self, input_text):
        input_field = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sidebar-input")))
        input_field.clear()
        input_field.send_keys(input_text)
        time.sleep(0.01)

        element_to_drag = self.find_element_by_text(input_text)
        
        fixed_position_x = 500
        fixed_position_y = 500
        #this position is arbatrary, can be changed based on use case, but I needed a static position to make sure that the elements combine correctly
        
        element_position_x = element_to_drag.location['x']
        element_position_y = element_to_drag.location['y']
        offset_x = fixed_position_x - element_position_x
        offset_y = fixed_position_y - element_position_y

        action = ActionChains(self.driver)
        action.click_and_hold(element_to_drag)
        action.move_to_element(element_to_drag)
        action.move_by_offset(offset_x, offset_y)
        action.release()
        action.perform()
        time.sleep(0.01)
        
        input_field.clear()
    
    def combine(self, input1, input2):
        self.drag(input1)
        self.drag(input2)

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "instances")))

        time.sleep(0.1)
        item_instances = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'item instance') and not(contains(@class, 'instance-hide'))]")

        if len(item_instances) != 3:
            click_target = self.driver.find_element(By.CLASS_NAME, "clear")
            click_target.click()
            return None
        else:
            text = item_instances[2].text.split('\n')[-1]
            click_target = self.driver.find_element(By.CLASS_NAME, "clear")
            click_target.click()
            return text
    def reset (self):
        #create a new driver to reset the game
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get("https://neal.fun/infinite-craft/")
        self.driver.implicitly_wait(10)
        

# Example usage
#url = "https://neal.fun/infinite-craft/"
#game = GameInstance(url)

#game.combine("Earth", "Water")
#game.combine("Plant", "Wind")

# Remember to close the browser once done
#game.driver.quit()