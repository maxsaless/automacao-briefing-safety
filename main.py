import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load environment variables
def load_env_variables():
    try:
        # Load variables from .env file
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("Environment variables loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading environment variables: {e}")
        raise

# Function to initialize the WebDriver with retry logic
def init_driver(retries=3):
    for attempt in range(retries):
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            logger.info("WebDriver initialized successfully.")
            return driver
        except WebDriverException as e:
            logger.warning(f"WebDriver initialization failed: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(2)
    logger.error("Failed to initialize WebDriver after retries.")
    raise

# Main function
if __name__ == '__main__':
    try:
        load_env_variables()  # Load environment variables
        driver = init_driver()  # Initialize the WebDriver
        # Main logic goes here
        # driver.get(os.getenv("URL"))
        # Perform your operations...  
        # driver.quit()
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
