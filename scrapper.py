# web scrapping for website 02
import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL = "https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/"



def scrape_cause_list(complex_name, court_number, date_str, case_type):

    driver = webdriver.Edge()
    driver.get(URL)
    wait = WebDriverWait(driver, 15)

    try:
        print(f"--- Scraping Cause List ---")
        print(f"Court Complex: {complex_name}")
        print(f"Court Number: {court_number}")
        print(f"Date: {date_str}")
        print(f"Case Type: {case_type}")
        print("---------------------------")


        print("Selecting court complex...")
        complex_dropdown = wait.until(EC.presence_of_element_located((By.ID, "est_code")))
        select_complex = Select(complex_dropdown)
        select_complex.select_by_visible_text(complex_name)
        print(f"'{complex_name}' selected.")

        print("Waiting for Court Number dropdown to populate...")


        court_dropdown_id = "court"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"#{court_dropdown_id} option:nth-child(2)")))
        print("Dropdown populated.")

        court_dropdown = driver.find_element(By.ID, court_dropdown_id)
        select_court = Select(court_dropdown)

        try:
            select_court.select_by_visible_text(court_number)
            print(f"'{court_number}' selected.")
        except NoSuchElementException:
            print(f"\n--- ERROR: Could not find Court Number ---")
            print(f"The text '{court_number}' was not found in the dropdown.")
            print("Please check for typos, extra spaces, or case sensitivity.")
            print("\nAvailable court names in the dropdown are:")

            options = select_court.options
            for option in options:
                if option.get_attribute("value"):
                    print(f"- {option.text.strip()}")

            raise


        time.sleep(1)


        print(f"Setting date to {date_str}...")
        date_input = wait.until(EC.presence_of_element_located((By.ID, "date")))
        driver.execute_script(f"arguments[0].value = '{date_str}';", date_input)
        print("Date set.")

        print(f"Selecting case type: {case_type}")
        if case_type.lower() == 'criminal':
            driver.find_element(By.ID, "chkCauseTypeCriminal").click()
        else:
            driver.find_element(By.ID, "chkCauseTypeCivil").click()
        print("Case type selected.")

        print("Handling CAPTCHA...")
        captcha_image = wait.until(EC.presence_of_element_located((By.ID, "siwp_captcha_image_0")))
        captcha_input = driver.find_element(By.ID, "siwp_captcha_value_0")
        submit_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-style-outline.accent-color.accent-border-color")

        captcha_image.screenshot('captcha.png')
        print("\nCAPTCHA image saved as 'captcha.png'.")
        user_captcha_text = input("Please look at the image and enter the CAPTCHA text: ")

        captcha_input.send_keys(user_captcha_text)
        submit_button.click()
        print("Form submitted. Waiting for results...")

        print("Waiting for results table to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "distTableContent")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results_table = soup.find('table', class_='distTableContent')

        if results_table:
            print("\n--- Scraping Results ---")
            print(results_table.get_text(separator='\n', strip=True))
            print("\nParsing logic needs to be implemented based on the results page structure.")
        else:
            print("\nCould not find the results table.")

    except TimeoutException:
        print("\n--- ERROR: Timed Out ---")
        print("The script timed out waiting for an element.")
        print("This could mean:")
        print(f"  1. The CAPTCHA you entered was incorrect.")
        print(f"  2. There is no cause list data for these settings.")
        print(
            f"  3. The 'Court Number' dropdown ID ('{court_dropdown_id}') is wrong. Please inspect the element and fix it.")
        print("Please re-run the script and try again.")
    except NoSuchElementException:

        print("Script stopped because the specified Court Number could not be found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Closing the browser.")
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A CLI tool to scrape the New Delhi District Court cause list.")

    parser.add_argument('--complex', type=str, required=True,
                        help='The name of the Court Complex (e.g., "Patiala House Court Complex").')
    parser.add_argument('--court', type=str, required=True,
                        help='The name of the Court (e.g., "1 Ms. Anju Bajaj Chandra...").')
    parser.add_argument('--date', type=str, required=True,
                        help='The cause list date in DD/MM/YYYY format.')
    parser.add_argument('--type', type=str, default='Civil', choices=['Civil', 'Criminal'],
                        help='The case type (Civil or Criminal).')

    args = parser.parse_args()

    scrape_cause_list(args.complex, args.court, args.date, args.type)