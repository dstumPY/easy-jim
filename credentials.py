HTML_CODE = "<p>CODE TO PUT ON YOUR PAGE</p>"
LOGIN_PAGE = "https://account.e.jimdo.com/de/accounts/login/"
LOGIN_USER = "yourmailadress@provider.com"
LOGIN_PASSWORD = "y0urs3cr3tp4ssw0rd"


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
