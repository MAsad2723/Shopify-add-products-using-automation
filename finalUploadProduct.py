import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Import the time module for adding delays


# Path to your ChromeDriver
chrome_driver_path = "path_to_chromedriver"  # Replace with your actual ChromeDriver path

# Set up Chrome options to connect to the debug instance
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Debug port from Step 1

# Initialize WebDriver with the debugging options
driver = webdriver.Chrome(service=Service(), options=options)

# Load the product data from JSON
data_file_path = r"data.json"  # Replace with your data.json file path
with open(data_file_path, 'r') as file:
    products = json.load(file)

try:
    # Open Shopify Admin Page (you should already be logged in)
    shopify_admin_url = "https://adyxth-qz.myshopify.com/admin/products/new"
    
    for product in products:
        driver.get(shopify_admin_url)

        # Fill in product details
        product_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='title']"))
        )
        product_name_field.send_keys(product["name"])

        # Add description
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "product-description_ifr"))
        )
        driver.switch_to.frame(iframe)

        editor_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tinymce"))
        )
        editor_body.clear()
        editor_body.send_keys(product["description"])
        driver.switch_to.default_content()

        # Upload media
        upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[span[contains(text(), 'Upload new')]]")
            )
        )
        upload_button.click()

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(product["media_path"])

        # Add a timeout after uploading the media
        time.sleep(10)  # Wait for 30 seconds to ensure media upload is completed

        # Add price
        product_price_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='price']"))
        )
        product_price_field.send_keys(product["price"])

        # Add compare at price
        product_compareAtPrice_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='compareAtPrice']"))
        )
        product_compareAtPrice_field.send_keys(product["compare_at_price"])

        # Add unit cost
        product_unitCost_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='unitCost']"))
        )
        product_unitCost_field.send_keys(product["unit_cost"])

        # Uncheck inventory tracking if required
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "InventoryTrackingTracked"))
        )
        if checkbox.is_selected():
            checkbox.click()

        # Save the product
        save_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Save']"))
        )
        save_button.click()

        print(f"Product '{product['name']}' added successfully!")
        time.sleep(3)

finally:
    # Close the browser when done (optional)
    driver.quit()


# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium_browser"