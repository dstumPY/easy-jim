import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credentials import HTML_CODE, LOGIN_PAGE, LOGIN_USER, LOGIN_PASSWORD


def website_login(driver_obj: webdriver, user_login_name: str, password_str: str):
    # find input fields for username and password andhttps://account.e.jimdo.com/de/accounts/login/
    # button to submit login credentials
    username_field = driver_obj.find_element_by_id("id_login")
    password_field = driver_obj.find_element_by_id("id_password")
    login_button = driver_obj.find_element_by_xpath("//div/button")

    # define actions on username
    actions = ActionChains(driver_obj)
    actions.move_to_element(username_field)
    actions.click(username_field)
    actions.send_keys(LOGIN_USER)
    # define actions on password
    actions.move_to_element(password_field)
    actions.click(password_field)
    actions.send_keys(LOGIN_PASSWORD)
    # define actions on login button
    actions.move_to_element(login_button)
    actions.click(login_button)

    # execute defined actions
    actions.perform()

    return driver_obj


def perform_web_actions(driver_obj: webdriver, html_code: str):
    # activate iframe object
    driver_obj.switch_to_frame("cms")

    # find input field and delete content
    driver_obj.find_element_by_id("cc-m-text-13822032930").clear()

    # click button to direct to the html input field
    additional_options_button = driver_obj.find_element_by_xpath(
        "//div[@id='cc-m-all-editor-13822032930']//button[@class='btn btn-sm btn-additional-settings btn-toggle-narrow']"
    )
    driver_obj.execute_script("arguments[0].click();", additional_options_button)

    # button to open html field
    html_edit_button = driver_obj.find_element_by_xpath(
        "//div[@id='cc-m-all-editor-13822032930']//button[@data-action='rteEditSource']"
    )
    driver_obj.execute_script("arguments[0].click();", html_edit_button)
    # find html field element and activate
    driver_obj.find_element_by_xpath(
        "//div[@class='mce-container mce-panel mce-floatpanel mce-window mce-in']//textarea[@class='mce-textbox mce-multiline mce-abs-layout-item mce-first mce-last']"
    ).click()
    # insert html code in input field
    driver_obj.find_element_by_xpath(
        "//div[@class='mce-container mce-panel mce-floatpanel mce-window mce-in']//textarea[@class='mce-textbox mce-multiline mce-abs-layout-item mce-first mce-last']"
    ).send_keys(HTML_CODE)
    # save html field and close
    driver_obj.find_element_by_xpath(
        "//div[@class='mce-widget mce-btn mce-primary mce-abs-layout-item mce-first mce-btn-has-text']//button[@role='presentation']"
    ).click()

    # activate date field again and save changes
    driver_obj.find_element_by_id("cc-m-text-13822032930").click()
    save_button = driver_obj.find_element_by_xpath(
        "//div[@id='cc-m-all-editor-13822032930']//button[@data-action='save']"
    )
    driver_obj.execute_script("arguments[0].click();", save_button)


def main():
    # define driver credentials and start page
    driver = webdriver.Chrome("/usr/bin/chromedriver")
    driver.get(LOGIN_PAGE)
    time.sleep(5)

    driver = website_login(driver, LOGIN_USER, LOGIN_PASSWORD)

    time.sleep(5)

    # get current url from redirected page
    driver.get(driver.current_url)
    driver.switch_to_default_content()

    # main interactions which includes inserting the html code
    perform_web_actions(driver, HTML_CODE)

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
