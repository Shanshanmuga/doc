# import json
# import os
# import pandas as pd
# import time
# from concurrent.futures import ThreadPoolExecutor
# from fastapi import FastAPI
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import logging
# import re
 
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
 
# # Load environment variables
# load_dotenv()
# CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
 
# # Directory to save JSON file
# json_file_path = 'C:\\Users\\Shanmugam.R\\Desktop\\Json files\\results3000to3300.json'
 
# # Load existing data from JSON file
# if os.path.exists(json_file_path):
#     with open(json_file_path, 'r') as file:
#         try:
#             existing_data = json.load(file)
#         except json.JSONDecodeError:
#             existing_data = {}
# else:
#     existing_data = {}
 
# app = FastAPI()
# driver = None
# last_login_time = None
 
# def initialize_driver():
#     global driver
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     prefs = {
#         "profile.managed_default_content_settings.images": 2,
#         "profile.managed_default_content_settings.stylesheets": 2,
#         "profile.managed_default_content_settings.javascript": 1
#     }
#     options.add_experimental_option("prefs", prefs)
 
#     service = Service(executable_path=CHROMEDRIVER_PATH)
#     driver = webdriver.Chrome(service=service)
#     #logger.info("WebDriver initialized.")
 
# def login(username, password, login_url):
#     global driver, last_login_time
 
#     driver.get(login_url)
#     driver.maximize_window()
#     time.sleep(2)
 
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-signin-basic-signin-form-username']"))
#     ).send_keys(username)
 
#     driver.find_element(By.XPATH, "//oj-button[@id='idcs-signin-basic-signin-form-submit']//div[@class='oj-button-label']").click()
#     time.sleep(2)
 
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-auth-pwd-input|input']"))
#     ).send_keys(password)
 
#     driver.find_element(By.XPATH, "//div[@class='oj-button-label']").click()
#     time.sleep(2)
 
#     last_login_time = datetime.now()
#     logger.info("Login successful.")
 
# def process_span_tag(index, my_texts):
#     global driver
   
#     span_xpath = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:gl14"]'
#     lab_xpath = f'//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:ol22"]'
#     date_xpath = '//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:wpfl1"]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span '
#     try:
       
       
#         span_tag = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, span_xpath))
#         )
#         span_tag.click()
#         span_text = span_tag.text
#         #logger.info(f"Span text: {span_text}")
#         href = driver.current_url
#         #logger.info(f"Link: {href}")
#         time.sleep(2)
 
#         doc_tag = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, lab_xpath))
#         )
#         doc_text = doc_tag.text
 
#         # Extract the Doc ID using regex
#         match = re.search(r'\(Doc ID (\d+\.\d+)\)', doc_text)
#         if (doc_id := match.group(1)) is not None:
#             logger.info(f"Extracted Doc ID: {doc_id}")
#         else:
#             doc_id = None
#             logger.warning(f"Doc ID not found in text: {doc_text}")
 
#         #Extract the date
#         date_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, date_xpath))
#         )
#         date_text = date_element.text
#         logger.info(f"Date: {date_text}")
#         time.sleep(1)
 
#         results_xpath = "//*[@id='kmPgTpl:sd_r1:0:dv_rDoc:0:pgl25']"
#         results = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, results_xpath))
#         )
#         soup = BeautifulSoup(results.get_attribute('innerHTML'), 'html.parser')
#         document_content = soup.get_text()
 
#         my_texts.append({
#             "url": href,
#             "document title": span_text,
#             "document id": doc_id,
#             "document": document_content,
#             "last update date": date_text,
#         })
 
#         driver.back()
#         time.sleep(2)
#     except (NoSuchElementException, StaleElementReferenceException) as e:
#         logger.warning(f"Span tag {index} not found or stale: {e}")
#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#     except Exception as e:
#         logger.error(f"Exception: {e}")
 
# def login_and_search(code, error_message):
#     global driver, last_login_time
#     username = "sathishkumar.s@focusrtech.com"
#     password = "Sathish@123"
#     search_text = code
#     login_url = "https://signon.oracle.com/signin"
#     search_url = "https://support.oracle.com/epmos/faces/Dashboard"
 
#     if driver is None or (last_login_time and datetime.now() - last_login_time > timedelta(minutes=5)):
#         if driver:
#             driver.quit()
#         initialize_driver()
#         login(username, password, login_url)
 
#     driver.get(search_url)
#     time.sleep(1)
 
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "pt1:svMenu:gsb:subFgsb:mGlobalSearch:pt_itG"))
#     ).send_keys(search_text + Keys.RETURN)
 
#     time.sleep(2)
   
#     try:
#         # Wait for the "Knowledge Base Search Results" section to be present
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='kmPgTpl:r1:0:mr1:r1:0:kbResult']"))
#         )
 
#         # Find the elements matching the pattern and count them
#         elements_xpath = '//*[contains(@id, "kmPgTpl:r1:0:mr1:r1:0:iR1") and contains(@id, "gl14")]'
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, elements_xpath))
#         )
       
#         # Find the elements and count them
#         elements = driver.find_elements(By.XPATH, elements_xpath)
#         time.sleep(1)
#         num_elements = len(elements)
       
#         logger.info(f"Number of matching elements: {num_elements}")
 
#         my_texts = []
#         if num_elements == 0:
#             logger.info("No matching elements found.")
#             existing_data[code] = {"documents": [], "error message": error_message}
#         else:
#             for index in range(num_elements):
#                 process_span_tag(index, my_texts)
#             existing_data[code] = {"documents": my_texts, "error message": error_message}
 
#         # Write to JSON file
#         with open(json_file_path, 'w') as file:
#             json.dump(existing_data, file, indent=4)
 
#         return existing_data[code]
 
#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#         existing_data[code] = {"documents": [], "error message": error_message}
#     except Exception as e:
#         logger.error(f"Exception: {e}")
#         existing_data[code] = {"documents": [], "error message": f"Exception: {e}"}
   
#     # Ensure to write to JSON file even if an error occurs
#     with open(json_file_path, 'w') as file:
#         json.dump(existing_data, file, indent=4)
   
#     return existing_data[code]
 
 
 
# @app.post("/search/")
# def search(code: str, error_message: str):
#     results = login_and_search(code, error_message)
#     return results
 
# if __name__ == "__main__":
#     import uvicorn
#     df = pd.read_excel("C:\\Users\\Shanmugam.R\\Desktop\\error_code.xlsx")
 
#     for index, row in df.iterrows():
#         error_code_message = row["Error_Code_Message"]
#         if ":" in error_code_message:
#             error_code, error_message = error_code_message.split(":")
#         else:
#             error_code = error_code_message
#             error_message = ""
 
#         error_code = error_code.strip()
#         error_message = error_message.strip()
#         print("\n")
#         print(f"Error Code: {error_code}")
       
#         search_result = search(error_code, error_message)
#         print(search_result)
 
#     uvicorn.run(app, host="127.0.0.1", port=8000)

##################################################### web scrapping #######################################################3

# import json
# import os
# import pandas as pd
# import time
# from concurrent.futures import ThreadPoolExecutor
# from fastapi import FastAPI
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import logging
# import re

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
 
# # Load environment variables
# load_dotenv()
# CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
 
# # Directory to save JSON file
# json_file_path = 'C:\\Users\\M1391\\Desktop\\results1.json'
 
# # Load existing data from JSON file
# if os.path.exists(json_file_path):
#     with open(json_file_path, 'r') as file:
#         try:
#             existing_data = json.load(file)
#         except json.JSONDecodeError:
#             existing_data = {}
# else:
#     existing_data = {}
 
# app = FastAPI()
# driver = None
# last_login_time = None
 
# def initialize_driver():
#     global driver
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     prefs = {
#         "profile.managed_default_content_settings.images": 2,
#         "profile.managed_default_content_settings.stylesheets": 2,
#         "profile.managed_default_content_settings.javascript": 1
#     }
#     options.add_experimental_option("prefs", prefs)
 
#     service = Service(executable_path=CHROMEDRIVER_PATH)
#     driver = webdriver.Chrome(service=service)
 
# def login(username, password, login_url):
#     global driver, last_login_time
 
#     driver.get(login_url)
#     driver.maximize_window()
#     time.sleep(2)
 
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-signin-basic-signin-form-username']"))
#     ).send_keys(username)
 
#     driver.find_element(By.XPATH, "//oj-button[@id='idcs-signin-basic-signin-form-submit']//div[@class='oj-button-label']").click()
#     time.sleep(2)
 
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-auth-pwd-input|input']"))
#     ).send_keys(password)
 
#     driver.find_element(By.XPATH, "//div[@class='oj-button-label']").click()
#     time.sleep(2)
 
#     last_login_time = datetime.now()
#     logger.info("Login successful.")
 
# def process_span_tag(index, my_texts):
#     global driver
   
#     span_xpath = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:gl14"]'
#     lab_xpath = f'//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:ol22"]'
#     date_xpath = '//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:wpfl1"]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span'
   
#     try:
#         span_tag = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, span_xpath))
#         )
#         span_tag.click()
#         span_text = span_tag.text
#         href = driver.current_url
#         time.sleep(2)
 
#         doc_tag = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, lab_xpath))
#         )
#         doc_text = doc_tag.text
 
#         # Extract the Doc ID using regex
#         match = re.search(r'\(Doc ID (\d+\.\d+)\)', doc_text)
#         if match:
#             doc_id = match.group(1)
#             logger.info(f"Extracted Doc ID: {doc_id}")
#         else:
#             doc_id = None
#             logger.warning(f"Doc ID not found in text: {doc_text}")
 
#         # Extract the date
#         try:
#             date_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, date_xpath))
#             )
#             date_text = date_element.text
#             logger.info(f"Date: {date_text}")
#         except TimeoutException:
#             logger.warning("Date not found, skipping this document.")
#             driver.back()
#             time.sleep(2)
#             return  # Skip this document and continue with the next
 
#         results_xpath = "//*[@id='kmPgTpl:sd_r1:0:dv_rDoc:0:pgl25']"
#         results = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, results_xpath))
#         )
#         soup = BeautifulSoup(results.get_attribute('innerHTML'), 'html.parser')
#         document_content = soup.get_text()
 
#         my_texts.append({
#             "url": href,
#             "document title": span_text,
#             "document id": doc_id,
#             "document": document_content,
#             "last update date": date_text,
#         })
 
#         driver.back()
#         time.sleep(2)
#     except (NoSuchElementException, StaleElementReferenceException) as e:
#         logger.warning(f"Span tag {index} not found or stale: {e}")
#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#     except Exception as e:
#         logger.error(f"Exception: {e}")
 
# def login_and_search(code, error_message):
#     global driver, last_login_time
#     username = "sathishkumar.s@focusrtech.com"
#     password = "Sathish@123"
#     search_text = code
#     login_url = "https://signon.oracle.com/signin"
#     search_url = "https://support.oracle.com/epmos/faces/Dashboard"
 
#     if driver is None or (last_login_time and datetime.now() - last_login_time > timedelta(minutes=5)):
#         if driver:
#             driver.quit()
#         initialize_driver()
#         login(username, password, login_url)
 
#     driver.get(search_url)
#     time.sleep(1)
 
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "pt1:svMenu:gsb:subFgsb:mGlobalSearch:pt_itG"))
#     ).send_keys(search_text + Keys.RETURN)
 
#     time.sleep(2)
#     # # Select the dropdown option
#     # select_element = WebDriverWait(driver, 10).until(
#     #     EC.presence_of_element_located((By.ID, "kmPgTpl:r1:0:mr1:s1:productSelectorNew:dc_sol1:itInputText::content"))
#     # )
#     # select_element.send_keys('Oracle E-Business Suite Technology Stack' + Keys.RETURN)
#     # time.sleep(6)
 
#     try:
#         # Wait for the "Knowledge Base Search Results" section to be present
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='kmPgTpl:r1:0:mr1:r1:0:kbResult']"))
#         )
 
#         # Find the elements matching the pattern and count them
#         elements_xpath = '//*[contains(@id, "kmPgTpl:r1:0:mr1:r1:0:iR1") and contains(@id, "gl14")]'
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, elements_xpath))
#         )
       
#         # Find the elements and count them
#         elements = driver.find_elements(By.XPATH, elements_xpath)
#         time.sleep(1)
#         num_elements = len(elements)
       
#         logger.info(f"Number of matching elements: {num_elements}")
 
#         my_texts = []
#         if num_elements == 0:
#             logger.info("No matching elements found.")
#             existing_data[code] = {"documents": [], "error message": error_message}
#         else:
#             for index in range(num_elements):
#                 process_span_tag(index, my_texts)
#             existing_data[code] = {"documents": my_texts, "error message": error_message}
 
#         # Write to JSON file
#         with open(json_file_path, 'w') as file:
#             json.dump(existing_data, file, indent=4)
 
#         return existing_data[code]
 
#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#         existing_data[code] = {"documents": [], "error message": error_message}
#     except Exception as e:
#         logger.error(f"Exception: {e}")
#         existing_data[code] = {"documents": [], "error message": f"Exception: {e}"}
   
#     # Ensure to write to JSON file even if an error occurs
#     with open(json_file_path, 'w') as file:
#         json.dump(existing_data, file, indent=4)
   
#     return existing_data[code]
 
# @app.post("/search/")
# def search(code: str, error_message: str):
#     results = login_and_search(code, error_message)
#     return results
 
# if __name__ == "__main__":
#     import uvicorn
#     df = pd.read_excel("C:\\Users\\M1391\\Desktop\\error_code.xlsx")
 
#     for index, row in df.iterrows():
#         error_code_message = row["Error_Code_Message"]
#         if ":" in error_code_message:
#             error_code, error_message = error_code_message.split(":",1)
#         else:
#             error_code = error_code_message
#             error_message = ""
 
#         error_code = error_code.strip()
#         error_message = error_message.strip()
#         print("\n")
#         print(f"Error Code: {error_code}")
       
#         search_result = search(error_code, error_message)
#         print(search_result)
 
#     uvicorn.run(app, host="127.0.0.1", port=8000)
 

######################################################## with-------keyword ##################################
import json
import os
import pandas as pd
import time
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

# Directory to save JSON file
json_file_path = 'C:\\Users\\M1391\\Desktop\\results1.json'

# Load existing data from JSON file
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as file:
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = {}
else:
    existing_data = {}

app = FastAPI()
driver = None
last_login_time = None

def initialize_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.javascript": 1
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

def login(username, password, login_url):
    global driver, last_login_time

    driver.get(login_url)
    driver.maximize_window()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-signin-basic-signin-form-username']"))
    ).send_keys(username)

    driver.find_element(By.XPATH, "//oj-button[@id='idcs-signin-basic-signin-form-submit']//div[@class='oj-button-label']").click()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-auth-pwd-input|input']"))
    ).send_keys(password)

    driver.find_element(By.XPATH, "//div[@class='oj-button-label']").click()
    time.sleep(2)

    last_login_time = datetime.now()
    logger.info("Login successful.")

def process_span_tag(index, keyword, my_texts):
    global driver

    # First, we check the span inside cl8 for the keyword
    span_xpath_cl8 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:cl8"]'
    span_xpath_gl14 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:gl14"]'

    try:
        span_tag_cl8 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, span_xpath_cl8))
        )
        span_text_cl8 = span_tag_cl8.text
        logger.info(f"Keyword : {span_text_cl8}")

        # span_tag_gl14 = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, span_xpath_gl14))
        # )
        # span_text_gl14 = span_tag_gl14.text
        # logger.info(f"title : {span_text_gl14}")


        # Check if the keyword is present in the span tag inside cl8
        if keyword in span_text_cl8:
            logger.info(f"Keyword '{keyword}' found in span text.")

            # Now attempt to click the link in gl14 if the keyword matches
            try:
                span_tag_gl14 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, span_xpath_gl14))
                )
                span_tag_gl14.click()
                href = driver.current_url
                title=span_tag_gl14.text
                time.sleep(2)

                lab_xpath = f'//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:ol22"]'
                date_xpath = '//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:wpfl1"]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span'

                try:
                    doc_tag = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, lab_xpath))
                    )
                    doc_text = doc_tag.text

                    match = re.search(r'\(Doc ID (\d+\.\d+)\)', doc_text)
                    doc_id = match.group(1) if match else None

                    try:
                        date_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, date_xpath))
                        )
                        date_text = date_element.text
                    except TimeoutException:
                        logger.warning("Date not found, skipping this document.")
                        driver.back()
                        time.sleep(2)
                        return

                    results_xpath = "//*[@id='kmPgTpl:sd_r1:0:dv_rDoc:0:pgl25']"
                    results = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, results_xpath))
                    )
                    soup = BeautifulSoup(results.get_attribute('innerHTML'), 'html.parser')
                    document_content = soup.get_text()

                    my_texts.append({
                        "url": href,
                        "document keyword": span_text_cl8,
                        "document title" :title,
                        "document id": doc_id,
                        "document": document_content,
                        "last update date": date_text,
                    })
                    driver.back()
                    time.sleep(2)
                except TimeoutException as e:
                    logger.warning(f"TimeoutException: {e}")
                    driver.back()
                    time.sleep(2)
            except TimeoutException as e:
                logger.error(f"TimeoutException: {e}")
            except Exception as e:
                logger.error(f"Exception: {e}")
        else:
            logger.info(f"Keyword '{keyword}' not found in span text.")
    except (NoSuchElementException, StaleElementReferenceException) as e:
        logger.warning(f"Span tag {index} not found or stale: {e}")
    except TimeoutException as e:
        logger.error(f"TimeoutException: {e}")
    except Exception as e:
        logger.error(f"Exception: {e}")

def login_and_search(code, error_message):
    global driver, last_login_time
    username = "sathishkumar.s@focusrtech.com"
    password = "Sathish@123"
    search_text = code
    keyword = "Oracle Cloud" #keyword
    login_url = "https://signon.oracle.com/signin"
    search_url = "https://support.oracle.com/epmos/faces/Dashboard"

    if driver is None or (last_login_time and datetime.now() - last_login_time > timedelta(minutes=5)):
        if driver:
            driver.quit()
        initialize_driver()
        login(username, password, login_url)

    driver.get(search_url)
    time.sleep(1)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "pt1:svMenu:gsb:subFgsb:mGlobalSearch:pt_itG"))
    ).send_keys(search_text + Keys.RETURN)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='kmPgTpl:r1:0:mr1:r1:0:kbResult']"))
        )

        elements_xpath = '//*[contains(@id, "kmPgTpl:r1:0:mr1:r1:0:iR1") and contains(@id, "gl14")]'
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, elements_xpath))
        )
        
        elements = driver.find_elements(By.XPATH, elements_xpath)
        time.sleep(1)
        num_elements = len(elements)
        
        logger.info(f"Number of matching elements: {num_elements}")

        my_texts = []
        if num_elements == 0:
            logger.info("No matching elements found.")
            existing_data[code] = {"documents": [], "error message": error_message}
        else:
            for index in range(min(num_elements, 10)):  # Process only the first 10 elements
                process_span_tag(index, keyword, my_texts)  # Pass the keyword here
            existing_data[code] = {"documents": my_texts, "error message": error_message}

        with open(json_file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

        return existing_data[code]

    except TimeoutException as e:
        logger.error(f"TimeoutException: {e}")
        existing_data[code] = {"documents": [], "error message": error_message}
    except Exception as e:
        logger.error(f"Exception: {e}")
        existing_data[code] = {"documents": [], "error message": f"Exception: {e}"}

    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return existing_data[code]

@app.post("/search/")
def search(code: str, error_message: str):
    results = login_and_search(code, error_message)
    return results
 
if __name__ == "__main__":
    import uvicorn
    df = pd.read_excel("C:\\Users\\M1391\\Desktop\\error_code.xlsx")
 
    for index, row in df.iterrows():
        error_code_message = row["Error_Code_Message"]
        if ":" in error_code_message:
            error_code, error_message = error_code_message.split(":",1)
        else:
            error_code = error_code_message
            error_message = ""
 
        error_code = error_code.strip()
        error_message = error_message.strip()
        print("\n")
        print(f"Error Code: {error_code}")
       
        search_result = search(error_code, error_message)
        print(search_result)
 
    uvicorn.run(app, host="127.0.0.1", port=8000)

#################################### with keyword and modules ##################################################

# import json
# import os
# import pandas as pd
# import time
# from fastapi import FastAPI
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import logging
# import re

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()
# CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

# # Directory to save JSON file
# json_file_path = 'C:\\Users\\M1391\\Desktop\\results1.json'

# # Load existing data from JSON file
# if os.path.exists(json_file_path):
#     with open(json_file_path, 'r') as file:
#         try:
#             existing_data = json.load(file)
#         except json.JSONDecodeError:
#             existing_data = {}
# else:
#     existing_data = {}

# app = FastAPI()
# driver = None
# last_login_time = None

# def initialize_driver():
#     global driver
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     prefs = {
#         "profile.managed_default_content_settings.images": 2,
#         "profile.managed_default_content_settings.stylesheets": 2,
#         "profile.managed_default_content_settings.javascript": 1
#     }
#     options.add_experimental_option("prefs", prefs)

#     service = Service(executable_path=CHROMEDRIVER_PATH)
#     driver = webdriver.Chrome(service=service)

# def login(username, password, login_url):
#     global driver, last_login_time

#     driver.get(login_url)
#     driver.maximize_window()
#     time.sleep(2)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-signin-basic-signin-form-username']"))
#     ).send_keys(username)

#     driver.find_element(By.XPATH, "//oj-button[@id='idcs-signin-basic-signin-form-submit']//div[@class='oj-button-label']").click()
#     time.sleep(2)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-auth-pwd-input|input']"))
#     ).send_keys(password)

#     driver.find_element(By.XPATH, "//div[@class='oj-button-label']").click()
#     time.sleep(2)

#     last_login_time = datetime.now()
#     logger.info("Login successful.")

# def process_span_tag(index, keyword_c18, module_c19, my_texts):
#     global driver

#     # Define the XPath expressions for cl8 (c18) and cl9 (c19)
#     span_xpath_cl8 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:cl8"]'  # For c18 (keyword)
#     span_xpath_cl9 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:cl9"]'  # For c19 (module)
#     span_xpath_gl14 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:gl14"]'  # The clickable link

#     try:
#         # Extract text from cl8 (c18)
#         span_tag_cl8 = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, span_xpath_cl8))
#         )
#         span_text_cl8 = span_tag_cl8.text
#         logger.info(f"Keyword : {span_text_cl8}")

#         # Extract text from cl9 (c19)
#         span_tag_cl9 = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, span_xpath_cl9))
#         )
#         span_text_cl9 = span_tag_cl9.text
#         logger.info(f"Module : {span_text_cl9}")

#         # Check if both the keyword (c18) and the module (c19) are present
#         if keyword_c18 in span_text_cl8 and module_c19 in span_text_cl9:
#             logger.info(f"Keyword '{keyword_c18}' found in cl8 and module '{module_c19}' found in cl9.")

#             # Now attempt to click the link in gl14 if both conditions are met
#             try:
#                 span_tag_gl14 = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, span_xpath_gl14))
#                 )
#                 span_tag_gl14.click()
#                 href = driver.current_url
#                 title = span_tag_gl14.text
#                 time.sleep(2)

#                 # Define XPaths for document content and date
#                 lab_xpath = f'//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:ol22"]'
#                 date_xpath = '//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:wpfl1"]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span'

#                 try:
#                     # Extract document content
#                     doc_tag = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.XPATH, lab_xpath))
#                     )
#                     doc_text = doc_tag.text

#                     # Extract document ID using regex
#                     match = re.search(r'\(Doc ID (\d+\.\d+)\)', doc_text)
#                     doc_id = match.group(1) if match else None

#                     # Extract date text
#                     try:
#                         date_element = WebDriverWait(driver, 10).until(
#                             EC.presence_of_element_located((By.XPATH, date_xpath))
#                         )
#                         date_text = date_element.text
#                     except TimeoutException:
#                         logger.warning("Date not found, skipping this document.")
#                         driver.back()
#                         time.sleep(2)
#                         return

#                     # Extract document content
#                     results_xpath = "//*[@id='kmPgTpl:sd_r1:0:dv_rDoc:0:pgl25']"
#                     results = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.XPATH, results_xpath))
#                     )
#                     soup = BeautifulSoup(results.get_attribute('innerHTML'), 'html.parser')
#                     document_content = soup.get_text()

#                     # Append data to my_texts
#                     my_texts.append({
#                         "url": href,
#                         "document keyword": span_text_cl8,
#                         "Module": span_text_cl9,
#                         "document title": title,
#                         "document id": doc_id,
#                         "document": document_content,
#                         "last update date": date_text,
#                     })

#                     # Navigate back after scraping
#                     driver.back()
#                     time.sleep(2)
#                 except TimeoutException as e:
#                     logger.warning(f"TimeoutException: {e}")
#                     driver.back()
#                     time.sleep(2)
#             except TimeoutException as e:
#                 logger.error(f"TimeoutException: {e}")
#             except Exception as e:
#                 logger.error(f"Exception: {e}")
#         else:
#             logger.info(f"Keyword '{keyword_c18}' not found in cl8 or module '{module_c19}' not found in cl9.")
#     except (NoSuchElementException, StaleElementReferenceException) as e:
#         logger.warning(f"Span tag {index} not found or stale: {e}")
#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#     except Exception as e:
#         logger.error(f"Exception: {e}")

# def login_and_search(code, error_message):
#     global driver, last_login_time
#     username = "sathishkumar.s@focusrtech.com"
#     password = "Sathish@123"
#     search_text = code
#     keyword = "Oracle E-Business Suite" #keyword
#     module = "Human captial management"
#     login_url = "https://signon.oracle.com/signin"
#     search_url = "https://support.oracle.com/epmos/faces/Dashboard"

#     if driver is None or (last_login_time and datetime.now() - last_login_time > timedelta(minutes=5)):
#         if driver:
#             driver.quit()
#         initialize_driver()
#         login(username, password, login_url)

#     driver.get(search_url)
#     time.sleep(1)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "pt1:svMenu:gsb:subFgsb:mGlobalSearch:pt_itG"))
#     ).send_keys(search_text + Keys.RETURN)

#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='kmPgTpl:r1:0:mr1:r1:0:kbResult']"))
#         )

#         elements_xpath = '//*[contains(@id, "kmPgTpl:r1:0:mr1:r1:0:iR1") and contains(@id, "gl14")]'
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, elements_xpath))
#         )
        
#         elements = driver.find_elements(By.XPATH, elements_xpath)
#         time.sleep(1)
#         num_elements = len(elements)
        
#         logger.info(f"Number of matching elements: {num_elements}")

#         my_texts = []
#         if num_elements == 0:
#             logger.info("No matching elements found.")
#             existing_data[code] = {"documents": [], "error message": error_message}
#         else:
#             for index in range(min(num_elements, 20)):  # Process only the first 10 elements
#                 process_span_tag(index, keyword,module, my_texts)  # Pass the keyword here
#             existing_data[code] = {"documents": my_texts, "error message": error_message}

#         with open(json_file_path, 'w') as file:
#             json.dump(existing_data, file, indent=4)

#         return existing_data[code]

#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#         existing_data[code] = {"documents": [], "error message": error_message}
#     except Exception as e:
#         logger.error(f"Exception: {e}")
#         existing_data[code] = {"documents": [], "error message": f"Exception: {e}"}

#     with open(json_file_path, 'w') as file:
#         json.dump(existing_data, file, indent=4)

#     return existing_data[code]

# @app.post("/search/")
# def search(code: str, error_message: str):
#     results = login_and_search(code, error_message)
#     return results
 
# if __name__ == "__main__":
#     import uvicorn
#     df = pd.read_excel("C:\\Users\\M1391\\Desktop\\error_code.xlsx")
 
#     for index, row in df.iterrows():
#         error_code_message = row["Error_Code_Message"]
#         if ":" in error_code_message:
#             error_code, error_message = error_code_message.split(":",1)
#         else:
#             error_code = error_code_message
#             error_message = ""
 
#         error_code = error_code.strip()
#         error_message = error_message.strip()
#         print("\n")
#         print(f"Error Code: {error_code}")
       
#         search_result = search(error_code, error_message)
#         print(search_result)
 
#     uvicorn.run(app, host="127.0.0.1", port=8000)



################################################## with keyword and modules and click to 8 times #################

# import json
# import os
# import pandas as pd
# import time
# from fastapi import FastAPI
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import logging
# import re

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()
# CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

# # Directory to save JSON file
# json_file_path = 'C:\\Users\\M1391\\Desktop\\results1.json'

# # Load existing data from JSON file
# if os.path.exists(json_file_path):
#     with open(json_file_path, 'r') as file:
#         try:
#             existing_data = json.load(file)
#         except json.JSONDecodeError:
#             existing_data = {}
# else:
#     existing_data = {}

# app = FastAPI()
# driver = None
# last_login_time = None

# def initialize_driver():
#     global driver
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     prefs = {
#         "profile.managed_default_content_settings.images": 2,
#         "profile.managed_default_content_settings.stylesheets": 2,
#         "profile.managed_default_content_settings.javascript": 1
#     }
#     options.add_experimental_option("prefs", prefs)

#     service = Service(executable_path=CHROMEDRIVER_PATH)
#     driver = webdriver.Chrome(service=service)

# def login(username, password, login_url):
#     global driver, last_login_time

#     driver.get(login_url)
#     driver.maximize_window()
#     time.sleep(2)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-signin-basic-signin-form-username']"))
#     ).send_keys(username)

#     driver.find_element(By.XPATH, "//oj-button[@id='idcs-signin-basic-signin-form-submit']//div[@class='oj-button-label']").click()
#     time.sleep(2)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@id='idcs-auth-pwd-input|input']"))
#     ).send_keys(password)

#     driver.find_element(By.XPATH, "//div[@class='oj-button-label']").click()
#     time.sleep(2)

#     last_login_time = datetime.now()
#     logger.info("Login successful.")

# def process_span_tag(index, keyword_c18, module_c19, my_texts):
#     global driver

#     # Define the XPath expressions for cl8 (c18) and cl9 (c19)
#     span_xpath_cl8 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:cl8"]'  # For c18 (keyword)
#     span_xpath_cl9 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:cl9"]'  # For c19 (module)
#     span_xpath_gl14 = f'//*[@id="kmPgTpl:r1:0:mr1:r1:0:iR1:{index}:gl14"]'  # The clickable link

#     try:
#         # Extract text from cl8 (c18)
#         span_tag_cl8 = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, span_xpath_cl8))
#         )
#         span_text_cl8 = span_tag_cl8.text
#         logger.info(f"Keyword : {span_text_cl8}")

#         # Extract text from cl9 (c19)
#         span_tag_cl9 = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, span_xpath_cl9))
#         )
#         span_text_cl9 = span_tag_cl9.text
#         logger.info(f"Module : {span_text_cl9}")

#         # Check if both the keyword (c18) and the module (c19) are present
#         if keyword_c18 in span_text_cl8 and module_c19 in span_text_cl9:
#             logger.info(f"Keyword '{keyword_c18}' found in cl8 and module '{module_c19}' found in cl9.")

#             # Now attempt to click the link in gl14 if both conditions are met
#             try:
#                 span_tag_gl14 = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, span_xpath_gl14))
#                 )
#                 span_tag_gl14.click()
#                 href = driver.current_url
#                 title = span_tag_gl14.text
#                 time.sleep(2)

#                 # Define XPaths for document content and date
#                 lab_xpath = f'//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:ol22"]'
#                 date_xpath = '//*[@id="kmPgTpl:sd_r1:0:dv_rDoc:0:wpfl1"]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span'

#                 try:
#                     # Extract document content
#                     doc_tag = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.XPATH, lab_xpath))
#                     )
#                     doc_text = doc_tag.text

#                     # Extract document ID using regex
#                     match = re.search(r'\(Doc ID (\d+\.\d+)\)', doc_text)
#                     doc_id = match.group(1) if match else None

#                     # Extract date text
#                     try:
#                         date_element = WebDriverWait(driver, 10).until(
#                             EC.presence_of_element_located((By.XPATH, date_xpath))
#                         )
#                         date_text = date_element.text
#                     except TimeoutException:
#                         logger.warning("Date not found, skipping this document.")
#                         driver.back()
#                         time.sleep(2)
#                         return

#                     # Extract document content
#                     results_xpath = "//*[@id='kmPgTpl:sd_r1:0:dv_rDoc:0:pgl25']"
#                     results = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.XPATH, results_xpath))
#                     )
#                     soup = BeautifulSoup(results.get_attribute('innerHTML'), 'html.parser')
#                     document_content = soup.get_text()

#                     # Append data to my_texts
#                     my_texts.append({
#                         "url": href,
#                         "document keyword": span_text_cl8,
#                         "Module": span_text_cl9,
#                         "document title": title,
#                         "document id": doc_id,
#                         "document": document_content,
#                         "last update date": date_text,
#                     })

#                     # Navigate back after scraping
#                     driver.back()
#                     time.sleep(2)
#                 except TimeoutException as e:
#                     logger.warning(f"TimeoutException: {e}")
#                     driver.back()
#                     time.sleep(2)
#             except TimeoutException as e:
#                 logger.error(f"TimeoutException: {e}")
#             except Exception as e:
#                 logger.error(f"Exception: {e}")
#         else:
#             logger.info(f"Keyword '{keyword_c18}' not found in cl8 or module '{module_c19}' not found in cl9.")
#     except (NoSuchElementException, StaleElementReferenceException) as e:
#         logger.warning(f"Span tag {index} not found or stale: {e}")
#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#     except Exception as e:
#         logger.error(f"Exception: {e}")

# def login_and_search(code, error_message):
#     global driver, last_login_time
#     username = "sathishkumar.s@focusrtech.com"
#     password = "Sathish@123"
#     search_text = code
#     keyword = "Oracle E-Business Suite"
#     module = "Human Capital Management"
#     login_url = "https://signon.oracle.com/signin"
#     search_url = "https://support.oracle.com/epmos/faces/Dashboard"

#     if driver is None or (last_login_time and datetime.now() - last_login_time > timedelta(minutes=5)):
#         if driver:
#             driver.quit()
#         initialize_driver()
#         login(username, password, login_url)

#     driver.get(search_url)
#     time.sleep(1)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "pt1:svMenu:gsb:subFgsb:mGlobalSearch:pt_itG"))
#     ).send_keys(search_text + Keys.RETURN)

#     try:
#         # Wait for the search results to appear
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='kmPgTpl:r1:0:mr1:r1:0:kbResult']"))
#         )
#         next_button_xpath = '//*[@id="kmPgTpl:r1:0:mr1:r1:0:kbNext"]'
#         my_texts = []

#         # Step 1: Click the "Next" button 8 times before scraping
#         for click_count in range(8):
#             try:
#                 logger.info(f"Clicking 'Next' button - {click_count + 1}/8")
#                 next_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, next_button_xpath))
#                 )
#                 next_button.click()
#                 time.sleep(2)  # Wait for the next page to load after clicking
#             except TimeoutException:
#                 logger.warning("Next button not clickable or no more pages to navigate.")
#                 break

#         # Step 2: Start scraping from the 8th page onwards
#         while True:  # Loop through the pages after the 8th click
#             try:
#                 # Fetch elements from the current page
#                 elements_xpath = '//*[contains(@id, "kmPgTpl:r1:0:mr1:r1:0:iR1") and contains(@id, "gl14")]'
#                 elements = WebDriverWait(driver, 10).until(
#                     EC.presence_of_all_elements_located((By.XPATH, elements_xpath))
#                 )
                
#                 num_elements = len(elements)
#                 logger.info(f"Number of matching elements after 8 clicks: {num_elements}")

#                 # Step 3: Scrape all links and match the keyword/module
#                 for index in range(num_elements):  # Process all links on the current page
#                     process_span_tag(index, keyword, module, my_texts)

#                 # Step 4: Check if the "Next" button is clickable to go to the next page
#                 try:
#                     next_button = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, next_button_xpath))
#                     )
#                     logger.info("Clicking 'Next' button to proceed to the next page.")
#                     next_button.click()
#                     time.sleep(2)  # Allow some time for the next page to load
#                 except TimeoutException:
#                     logger.info("No more 'Next' button found. Ending pagination.")
#                     break  # No more "Next" button, so stop the loop
#             except TimeoutException as e:
#                 logger.error(f"TimeoutException: {e}")
#                 break
#             except Exception as e:
#                 logger.error(f"Exception: {e}")
#                 break

#         # Store the results after scraping
#         existing_data[code] = {"documents": my_texts, "error message": error_message}

#         with open(json_file_path, 'w') as file:
#             json.dump(existing_data, file, indent=4)

#         return existing_data[code]

#     except TimeoutException as e:
#         logger.error(f"TimeoutException: {e}")
#         existing_data[code] = {"documents": [], "error message": error_message}
#     except Exception as e:
#         logger.error(f"Exception: {e}")
#         existing_data[code] = {"documents": [], "error message": f"Exception: {e}"}

#     with open(json_file_path, 'w') as file:
#         json.dump(existing_data, file, indent=4)

#     return existing_data[code]

# @app.post("/search/")
# def search(code: str, error_message: str):
#     results = login_and_search(code, error_message)
#     return results
 
# if __name__ == "__main__":
#     import uvicorn
#     df = pd.read_excel("C:\\Users\\M1391\\Desktop\\error_code.xlsx")
 
#     for index, row in df.iterrows():
#         error_code_message = row["Error_Code_Message"]
#         if ":" in error_code_message:
#             error_code, error_message = error_code_message.split(":",1)
#         else:
#             error_code = error_code_message
#             error_message = ""
 
#         error_code = error_code.strip()
#         error_message = error_message.strip()
#         print("\n")
#         print(f"Error Code: {error_code}")
       
#         search_result = search(error_code, error_message)
#         print(search_result)
 
#     uvicorn.run(app, host="127.0.0.1", port=8000)