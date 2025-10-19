# web scraping for website number 01
import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_case_status_by_cnr(cnr_number):

    driver = webdriver.Edge()
    driver.get(
        "https://services.ecourts.gov.in/ecourtindia_v6/?&app_token=6f31c56d2b77a35f50ae8d0319c56e2706a123cab6441f39e0c0ef7c2b487860")

    try:

        wait = WebDriverWait(driver, 10)

        print("Waiting for CNR form elements to load...")


        cnr_input_selector = (By.CLASS_NAME, 'cinumber')


        captcha_image_id = 'div_captcha_cnr'
        captcha_input_id = 'fcaptcha_code'
        submit_button_id = 'searchbtn'
        print("Looking for CNR input box...")
        cnr_input_box = wait.until(EC.presence_of_element_located(cnr_input_selector))
        print("CNR input box found.")


        captcha_image = driver.find_element(By.ID, captcha_image_id)
        captcha_text_box = driver.find_element(By.ID, captcha_input_id)
        submit_button = driver.find_element(By.ID, submit_button_id)

        captcha_image.screenshot('captcha.png')
        print("CAPTCHA image saved as 'captcha.png'. Please look at the image.")
        user_captcha_text = input("Enter the CAPTCHA text you see: ")


        cnr_input_box.send_keys(cnr_number)
        captcha_text_box.send_keys(user_captcha_text)
        submit_button.click()

        print("Waiting for results page to load...")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        case_details_div = soup.find('div',
                                     class_='table case_details_table table-bordered')

        if not case_details_div:
            print("Could not find case details. The CAPTCHA may have been wrong or the CNR invalid.")

            input("Press Enter to close the browser...")
            return


        listing_info = case_details_div.find('div', class_='fw-bold')

        if listing_info and ("today" in listing_info.text.lower() or "tomorrow" in listing_info.text.lower()):
            print("\n✅ Case is listed for today or tomorrow!")

            print("\n--- Full Case Details ---")
            print(case_details_div.text.strip())
            print("-------------------------")

            registration_number = listing_info.find('span', class_='serial_no_class').text.strip()
            court_number = listing_info.find('div', class__='court_name_class').text.strip()

            result = {
                'cnr': cnr_number,
                'status': 'Listed',
                'registration_number': registration_number,
                'court_number': court_number,
            }
        else:
            print("\nℹ️ Case is not listed for today or tomorrow.")


            print("\n--- Full Case Details ---")
            print(case_details_div.text.strip())
            print("-------------------------")


            result = {'cnr': cnr_number, 'status': 'Not Listed Today/Tomorrow'}

        print(json.dumps(result, indent=2))
        with open(f"{cnr_number}_data.json", "w") as f:
            json.dump(result, f, indent=2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:

        print("Script finished. The browser will close after you press Enter.")
        input("Press Enter to close the browser...")

        print("Closing the browser.")
        driver.quit()


def download_cause_list():

    driver = webdriver.Chrome()
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
    print("Attempting to download the cause list...")

    try:

        cause_list_link = driver.find_element(By.LINK_TEXT, "COPY OF ORDER")
        cause_list_link.click()


        print("Cause list logic is not yet implemented. You need to add the selectors.")


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A CLI tool to scrape eCourts India services.")


    parser.add_argument('--cnr', type=str, help='The CNR number of the case to check.')
    parser.add_argument('--causelist', action='store_true', help="Download today's cause list.")

    args = parser.parse_args()

    if args.cnr:
        get_case_status_by_cnr(args.cnr)
    elif args.causelist:
        download_cause_list()
    else:
        print("No action specified. Please provide an argument.")
        parser.print_help()