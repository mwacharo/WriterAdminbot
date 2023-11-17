from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

import time

# Set up the browser
browser = webdriver.Chrome()

try:
    # Open the website
    print("Opening the website...")
    browser.get("https://writer.writersadmin.com/")

    # Log in to the website (replace with your actual login credentials)
    email = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "password")))

    email.send_keys("mwacharomwanyolo@gmail.com")
    password.send_keys("John@001")

    login_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    print("Logged in successfully.")

    # Wait for the notification modal to appear (modify as needed)
    try:
        notification_modal = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-header')))
        close_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
        ActionChains(browser).move_to_element(close_button).click().perform()
        WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-header')))
        print("Notification modal closed.")
    except TimeoutException as e:
        print(f"Notification modal not found: {e}. Proceeding with the script.")

    # Define the "retry_operation" function
    def retry_operation(operation, max_retries=10):
        for _ in range(max_retries):
            try:
                operation()
                return
            except TimeoutException as e:
                print(f"Timeout exception: {e}. Retrying...")
        print(f"Operation failed after {max_retries} retries.")

    # Click on the "Available" menu item
    print("Clicking on the 'Available' menu item...")
    available_menu_item = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@id='side-menu-item-available-group']/a"))
    )
    available_menu_item.click()

    # Define the "New" link operation
    def click_new_link():
        new_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/orders/available/']"))
        )
        new_link.click()

    # Use the retry_operation function for clicking the "New" link
    print("Clicking on the 'New' link...")
    retry_operation(click_new_link)

    # (Previous code...)

    # Wait for the top-most order to be present
    print("Waiting for the top-most order to be present...")
    top_most_order = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[@class='single-order']"))
    )

    # Click on the top-most order
    print("Clicking on the top-most order...")
    top_most_order.click()
    print("Clicked on the top-most order...")

    # Wait for the "Request / Bid" button to be clickable
    print("Waiting for the btn-take to be present...")
    btn_take = WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='btn-take']"))
    )
        # Click on the btn_take
    print("Clicking on the  btn_take...")
    btn_take.click()
    print("Clicked on the  btn_take...")




    request_bid_button = WebDriverWait(browser, 60).until(
         EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn-take'))
    )


   

except TimeoutException as e:
    print(f"TimeoutException: {e}")

finally:
        # Wait for 12 hours before closing the browser
    print("Waiting for 12 hours before closing the browser...")
    time.sleep(12 * 60 * 60)  # 12 hours in seconds

    # Quit the browser
    print("Closing the browser...")
    browser.quit()

