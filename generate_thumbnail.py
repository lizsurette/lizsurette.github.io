import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def generate_thumbnail():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=800,600")  # Set window size
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Get the absolute path to the HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "app", "static", "snake-thumbnail.html")
        file_url = f"file://{html_path}"
        
        # Load the HTML file
        driver.get(file_url)
        
        # Wait for the page to load
        time.sleep(1)
        
        # Take a screenshot
        screenshot_path = os.path.join(current_dir, "app", "static", "projects", "snake-game.jpg")
        driver.save_screenshot(screenshot_path)
        
        print(f"Thumbnail generated successfully at: {screenshot_path}")
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    generate_thumbnail() 