
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime as dt
import sys
from glob import glob
import os

"""
Developed by AlexeyVolovinin
Github: https://github.com/AlexeyVolovinin
Pinterest: https://de.pinterest.com/atomacssowtware/
Support author: http://sites.google.com/view/color-mosaic-coloring-pages/%D1%85%D0%B0%D1%82%D0%BD%D1%8F%D1%8F-%D1%81%D1%82%D0%B0%D1%80%D0%BE%D0%BD%D0%BA%D0%B0
"""

config = {
    "board_XPATH": """//*[@id="__PWS_ROOT__"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div""",
    "title_XPATH": """//*[@id="pin-draft-title-b60b375e-df6b-4b57-a713-3d0c57198203"]""",
    "description_XPATH": """//*[@id="__PWS_ROOT__"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/div[1]""",
    "alt_button_XPATH": """//*[@id="__PWS_ROOT__"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[4]/div/button""",
    "alt_textarea_XPATH": """//*[@id="pin-draft-alttext-27f8ae11-72c1-4450-beb4-e42298634df3"]""",
    "publish_button_XPATH": """//*[@id="__PWS_ROOT__"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div""",
    "link_XPATH": """//*[@id="pin-draft-link-32d02298-0234-4a1f-a663-01b5b0c322cb"]""",
    "chrome_binary_location": "",
    "driver_exit_timeout": 5
}

class PinsStorage:
    """_summary_
    Reading, creating, checking data. 
    """
    def __init__(self, file: str, filetype: str) -> None:
        self.filetype = filetype
        if filetype == '.json':
            from json import loads
            self.file = loads(open(file, encoding='utf-8').read())['pin']
            self.lenght = len(self.file)  
        elif filetype == '.csv':
            self.file = open(file, encoding='utf-8').read().splitlines()[1:]
            self.lenght = len(self.file)  
        else:
            raise Exception(f'File format is not supported.')

    def load_data_from_pins(self, data: list) -> None:
        """_summary_: Create a list with pin ata 
        Args:
            data (list): 
                required* - title (str): Title of the pin. 
                required* - description (str): Description of the pin.
                required* - alt_text (str): Alt text of the pin.
                - link (str): Link of the pin.
                - date (str): Date of the pin.
                - pinboard (str): Pinboard name.
                - file_path: File path of the pin.
        """
        self.pinboard = str(data[0])
        self.file_path = os.path.abspath(str(data[1])) 
        self.title = str(data[2])
        self.description = str(data[3]) 
        self.alt_text = str(data[4])
        self.link = str(data[5])
        self.date = str(data[6])

    def validate_pins_data(self, format: str = '%d/%m/%Y %H:%M') -> bool:
        """_summary_
        - check required files
        - check length of data

        Args:
            format (_type_, optional): 
            - date (str): 01/01/2025 12:00 or 01/01/2025 12:00, 
                Hour: "XX:00" or "XX:30".
            - desription: 500 max
            - title: 100 max
            - alt_text: 100max

        Returns:
            bool: Correct format (True)
                  Incorrect format (False)
        """
        for data in [self.pinboard, self.file_path, self.title]:
            if data == '':
                return False, 'Missing required value.'
        if len(self.description) > 500 or len(self.alt_text) > 500:
            return False, 'Description or alt text is too long ' + \
                '(maximum 500 characters long).'
        if len(self.title) > 100:
            return False, 'Title is too long (maximum 100 characters long).'
        if not os.path.isfile(os.path.abspath(self.file_path)):
            return False, 'File doesn\'t exist.'
        if self.date != '':
            try:
                now = dt.strptime(dt.strftime(dt.now(), format), format)
                if (dt.strptime(self.date, format)
                        - now).total_seconds() / 60 > 20160:
                    return False, 'Difference must be less than 14 days.'
                if now > dt.strptime(self.date, format):
                    return False, 'Starting date has passed.'
            except ValueError:
                return False, 'Date format is invalid.'
            if self.date[-2:] != '30' and self.date[-2:] != '00':
                return False, 'Time must be every 30 minutes.'
        return True, None

    def format_data(self, number: int) -> None:
        self.number = number
        if self.filetype in ('.json', '.csv'):
            eval(f'self{self.filetype}_file()')
        else:
            raise Exception(f'File format is not supported.')

    def json_file(self) -> None:
        pin_data = self.file[self.number]
        self.load_data_from_pins([pin_data[data].strip() for data in pin_data])

    def csv_file(self) -> None:
        pin_data = self.file[self.number].split(';;')
        self.load_data_from_pins([data.strip() for data in pin_data])


class Pinterest:
    def __init__(self, email: str, password: str) -> None:
        """Set path of used file and start webdriver."""
        self.email = email  
        self.password = password  
        self.webdriver_path = os.path.abspath('settings/chromedriver')
        self.driver = self.webdriver()  
        self.login_url = 'https://www.pinterest.com/login/'
        self.upload_url = 'https://www.pinterest.com/pin-builder/'

    def webdriver(self):
        options = webdriver.ChromeOptions()  
        options.add_argument('--lang=en')  
        options.add_argument('log-level=3')  
        options.add_argument('--mute-audio')  
        options.binary_location = config["chrome_binary_location"]
        driver = webdriver.Chrome(service=Service(  
            self.webdriver_path), options=options)  
        driver.maximize_window()  
        return driver

    def clickable(self, element: str) -> None:
        """Click on element if it's clickable using Selenium."""
        WDW(self.driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, element))).click()

    def visible(self, element: str):
        """Check if element is visible using Selenium."""
        return WDW(self.driver, 15).until(EC.visibility_of_element_located(
            (By.XPATH, element)))

    def send_keys(self, element: str, keys: str) -> None:
        """Send keys to element if it's visible using Selenium."""
        try:
            self.visible(element).send_keys(keys)
        except Exception:  
            self.driver.execute_script(f'arguments[0].innerText = "{keys}"',
                                       self.visible(element))

    def window_handles(self, window_number: int) -> None:
        """_summary_
        Check for window handles and wait until a specific tab is opened.
        Args:
            window_number (int): _description_
        """
        WDW(self.driver, 30).until(lambda _: len(
            self.driver.window_handles) == window_number + 1)
        
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def login(self) -> None:

        try:
            print('Login to Pinterest.', end=' ')
            self.driver.get(self.login_url)  
            
            self.send_keys('//*[@id="email"]', self.email)
            self.send_keys('//*[@id="password"]', self.password)
            self.clickable(  
                '//div[@data-test-id="registerFormSubmitButton"]/button')
            WDW(self.driver, 30).until(  
                lambda _: self.driver.current_url != self.login_url)
            print(f'Logged.\n')
        except Exception:
            sys.exit(f'Failed.\n')

    def upload_pins(self, pin: int) -> None:
        """Upload pins one by one on Pinterest."""
        try:
            print(f'Uploading pins n°{pin + 1}/{data.lenght}.', end=' ')
            self.driver.get(self.upload_url)  
            self.driver.implicitly_wait(5)  
            
            self.clickable(config["board_XPATH"])
            try:
                self.clickable(  
                    f'//div[text()="{data.pinboard}"]/../../..')
            except Exception:
                raise Exception('Pinboard name is invalid.')
                
            self.driver.find_element(by=By.XPATH, value="//input[contains(@id, 'media-upload-input')]").send_keys(data.file_path)
            
            
            title = self.driver.find_elements(By.CSS_SELECTOR, "textarea")[0]
            title.send_keys(data.title)
            self.send_keys(  
                config['description_XPATH'], data.description)
            self.clickable(  
                config["alt_button_XPATH"])
            
            alt_text = self.driver.find_elements(By.CSS_SELECTOR, "textarea")[1]
            alt_text.send_keys(data.alt_text)
            
            link = self.driver.find_elements(By.CSS_SELECTOR, "textarea")[2]
            link.send_keys(data.link)
            if len(data.date) > 0:
                date, time = data.date.split(' ')
                
                self.clickable('//label[contains(@for, "pin-draft-'
                                       'schedule-publish-later")]')
                
                self.clickable('//input[contains(@id, "pin-draft-'
                                       'schedule-date-field")]/../../../..')
                
                month_name = dt.strptime(date, "%d/%m/%Y").strftime("%B")
                
                day = data.date[:2][1] if \
                    data.date[:2][0] == '0' else data.date[:2]
                self.clickable('//div[contains(@aria-label, '
                                       f'"{month_name} {day}")]')
                
                self.clickable('//input[contains(@id, "pin-draft-'
                                       'schedule-time-field")]/../../../..')
                
                self.clickable(f'//div[contains(text(), "{time} AM")]')
            self.clickable(  
                config['publish_button_XPATH'])
            
            self.visible('//div[@role="dialog"]')
            print('Uploaded.')
            sleep(config["driver_exit_timeout"])
            self.driver.quit()
        except Exception as error:
            print(f'Failed. {error}')

def read_file(file_: str, question: str) -> str:
    """Read file or ask for data to write in text file."""
    if not os.path.isfile(f'settings/{file_}.txt'):
        open(f'settings/{file_}.txt', 'a')  
    with open(f'settings/{file_}.txt', 'r+', encoding='utf-8') as file:
        text = file.read()  
        if text == '':  
            text = input(question)  
            if input(f'Do you want to save your {file_} in '
                     'a text file? (y/n) ').lower() != 'y':
                print(f'Not saved.')
            else:
                file.write(text)  
                print(f'Saved.')
        return text


def data_file() -> str:
    """_summary_
    Read the data folder and extract files with pins.
    Returns:
        str: data readed from publish
    """
    while True:
        file_number, files_list = 0, []
        print(f'\nChoose your file:\n0 - Browse a file on PC.')
        for files in [glob(f'publish/{extension}')  
                      for extension in ['*.json', '*.csv', '*.xlsx']]:
            for file in files:
                file_number += 1
                files_list.append(file)
                print(f'{file_number} - {os.path.abspath(file)}')
        answer = input('File number: ')
        cls()  
        if not answer.isdigit():  
            print(f'Answer must be an integer.')
        elif int(answer) == 0:  
            print(f'Browsing on your computer...')
            from tkinter import Tk  
            from tkinter.filedialog import askopenfilename
            Tk().withdraw()  
            return askopenfilename(filetypes=[('', '.json .csv .xlsx')])
        elif int(answer) <= len(files_list):
            return files_list[int(answer) - 1]  
        print(f'File doesn\'t exist.')


if __name__ == '__main__':

    print(
        """
Developed by AlexeyVolovinin
Github: https://github.com/AlexeyVolovinin
Pinterest: https://de.pinterest.com/atomacssowtware/
Support author: http://sites.google.com/view/color-mosaic-coloring-pages/%D1%85%D0%B0%D1%82%D0%BD%D1%8F%D1%8F-%D1%81%D1%82%D0%B0%D1%80%D0%BE%D0%BD%D0%BA%D0%B0
"""
    )

    with open("settings/browser.txt", "r", encoding="utf-8") as file:
        config["chrome_binary_location"] = file.read()

    if config["chrome_binary_location"] == "":
        def find_browser(binary_name):
            paths = {
            'win32': [f"C:\Program Files\{binary_name}\{binary_name}.exe",
            f"C:\Program Files (x86)\{binary_name}\{binary_name}.exe"],
            'darwin': [f"/Applications/{binary_name}.app/Contents/MacOS/{binary_name}"],
            'linux': [f"/usr/bin/{binary_name}", f"/usr/local/bin/{binary_name}"]
            }.get(sys.platform, [])

            for path in paths:
                if os.path.exists(path): return path
                return None
            
        chrome_path = find_browser("google-chrome")
        brave_path = find_browser("brave-browser")
        chromium_path = find_browser("chromium")
        selected_browser_path = next((path for path in [chrome_path, brave_path, chromium_path] if path), None)
        with open("settings/browser.txt", "w", encoding="utf-8") as file:
            config["chrome_binary_location"] = selected_browser_path
            file.write(selected_browser_path)
        if chrome_path:
            print("Using Chrome:", chrome_path)
        elif brave_path:
            print("Using Brave:", brave_path)
        elif chromium_path:
            print("Using Chromium:", chromium_path)
        else:
            print("Browser Undefined")
            print("Please, install browser")

    email = read_file('email', '\nWhat is your Pinterest email? ')
    password = read_file('password', '\nWhat is your Pinterest password? ')

    file = data_file()  
    data = PinsStorage(file, os.path.splitext(file)[1])  
    pinterest = Pinterest(email, password)  
    pinterest.login()

    for pin in range(data.lenght):
        data.format_data(pin)  
        check = data.validate_pins_data()
        if not check[0]:
            print(f'Data of pin n°{pin + 1}/{data.lenght} is incorrect.'
                  f'\nError: {check[1]}')
        else:
            pinterest.upload_pins(pin)  
