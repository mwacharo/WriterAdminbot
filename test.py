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

    # Repeat for each order
    while True:
        # Wait for the top-most order to be present
        print("Waiting for the top-most order to be present...")
        top_most_order = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='single-order']"))
        )

        # Click on the top-most order
        print("Clicking on the top-most order...")
        top_most_order.click()
        print("Clicked on the top-most order...")

        # opens to a new page
        new_window_handle = browser.window_handles[1]
        browser.switch_to.window(new_window_handle)

        # Wait for the "Request / Bid" button to be clickable
        print("Waiting for the btn-take to be present...")
        btn_take = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='btn-take']"))
        )

        # Click on the btn_take
        print("Clicking on the btn_take...")
        btn_take.click()
        print("Clicked on the btn_take...")

        # Wait for the bidding modal to be present
        bidding_modal = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "modal-bidding-form"))
        )

        # Wait for the "Message" textarea in the bidding modal
        description_input = WebDriverWait(bidding_modal, 30).until(
            EC.presence_of_element_located((By.NAME, "description"))
        )

        # Clear and input your bid message
        print("Filling in the bid form with a predefined message...")
        description_input.send_keys(
            "I have reviewed the provided instructions and understand the requirements. Rest assured, I am committed to delivering top-notch work, drawing upon my expertise from successfully completing prior tasks. Your project will be approached with the utmost professionalism and dedication to ensure exceptional quality. I am confident that my experience positions me well to meet and exceed your expectations. Kindly consider me."
        )
        print("Message filled")

        # Locate and click the "Place bid" button
        place_bid_button = WebDriverWait(bidding_modal, 30).until(
            EC.element_to_be_clickable((By.ID, "btn-request"))
        )
        place_bid_button.click()

        print("Bid placed successfully!")

        # Switch back to the original window
        browser.switch_to.window(browser.window_handles[0])

        # Refresh the page every 2 minutes while in the orders window
        refresh_interval = 30  # seconds
        print(f"Refreshing the page after {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        browser.refresh()

finally:
    # Wait for 12 hours before closing the browser
    print("Waiting for 12 hours before closing the browser...")
    time.sleep(12 * 60 * 60)  # 12 hours in seconds

    print("Closing the browser...")
    browser.quit()
