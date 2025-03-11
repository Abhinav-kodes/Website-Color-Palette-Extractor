import os
import random
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# List of user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
]
def run_img_to_hex_script():
    try:
        result = subprocess.run(['python', 'img_to_hex.py'], check=True, capture_output=True, text=True)
        print("img_to_hex.py output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running img_to_hex.py: {e}")
        print(f"Error output: {e.stderr}")

# Set up Chrome options
options = Options()
options.add_argument(f'user-agent={random.choice(user_agents)}')
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")  # Set initial window size

# Set up Chrome service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to the webpage
    url = 'https://www.youtube.com/'
    driver.get(url)

    # Wait for the cookie consent button to appear and click it
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
        )
        consent_button.click()
        print("Cookie consent accepted.")
    except TimeoutException:
        print("Cookie consent button not found or not clickable.")

    # Wait for animations and dynamic content to load
    time.sleep(5)

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Define the directory path
    imgs_dir = os.path.join(os.getcwd(), 'imgs')

    # Create the directory if it doesn't exist
    if not os.path.exists(imgs_dir):
        os.makedirs(imgs_dir)

    # List to hold screenshots
    screenshots = []

    # Scroll through the page and capture screenshots
    for offset in range(0, total_height+500, viewport_height):
        driver.execute_script(f"window.scrollTo(0, {offset});")
        time.sleep(1)  # Allow time for the page to render
        screenshot_path = os.path.join(imgs_dir, f'screenshot_{offset}.png')
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)

    # Capture any remaining part of the page
    if total_height % viewport_height != 0:
        driver.execute_script(f"window.scrollTo(0, {total_height - viewport_height});")
        time.sleep(1)
        screenshot_path = os.path.join(imgs_dir, f'screenshot_{total_height}.png')
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)

    # Stitch screenshots together
    stitched_image_path = os.path.join(imgs_dir, 'fullpage_screenshot.png')
    images = [Image.open(screenshot) for screenshot in screenshots]
    total_width = images[0].width
    combined_image = Image.new('RGB', (total_width, total_height+500))
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    combined_image.save(stitched_image_path)
    print(f"Full-page screenshot saved at: {stitched_image_path}")

    # Clean up individual screenshots
    for screenshot in screenshots:
        os.remove(screenshot)

finally:
    # Close the browser
    driver.quit()
run_img_to_hex_script()