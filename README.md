Here is the content for your `README.md` file.

-----

# New Delhi District Court - Cause List Scraper

This project is a Python script that scrapes the daily cause list from the New Delhi District Court website.

It's a command-line tool that automates the process of filling out the web form, including selecting the court complex, the specific court/judge, the date, and the case type. It's designed to handle the dynamic dropdowns and the manual CAPTCHA required by the site.

## 🚀 Features

  * **Command-Line Interface (CLI):** Easy to use with simple arguments.
  * **Dynamic Form Handling:** Automatically selects the "Court Complex" and then waits for the dependent "Court Number" dropdown to populate before selecting from it.
  * **JavaScript Injection:** Sets the "Cause List Date" field, even though it's marked as 'readonly'.
  * **Manual CAPTCHA Helper:** Pauses the script, saves a screenshot of the CAPTCHA (`captcha.png`), and waits for you to type the solution into the terminal.
  * **Robust Waiting:** Uses `WebDriverWait` to reliably wait for page elements to load, preventing common timing errors.
  * **Smart Error Handling:** If you provide a `--court` name that doesn't exist, the script will print all *available* court names for that complex, helping you find the correct one.

## 🛠️ Tech Stack

  * **Python 3**
  * **Selenium:** For automating the web browser and interacting with form elements.
  * **BeautifulSoup4:** For parsing the HTML of the results page.
  * **argparse:** For creating the command-line interface.

## Requirements

  * Python 3.x
  * Microsoft Edge (The script is currently set to use `webdriver.Edge()`)
  * The required Python libraries.

## ⚙️ Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/YourUsername/YourProjectName.git
    cd YourProjectName
    ```

2.  **Install the required Python libraries:**

    ```bash
    pip install selenium beautifulsoup4
    ```

3.  **Ensure you have the Edge WebDriver:**
    Selenium 4's `selenium-manager` should handle this automatically. If it doesn't, you may need to download the [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and ensure it's in your system's PATH.

## Usage

You must run the script from your terminal and provide the required arguments.

### **Command-Line Arguments**

  * `--complex` (Required): The full name of the Court Complex (e.g., `"Patiala House Court Complex"`).
  * `--court` (Required): The full name of the Court/Judge (e.g., `"1 Ms. Anju Bajaj Chandna - Principal District and Sessions Judge"`).
  * `--date` (Required): The date you want to search for, in `DD/MM/YYYY` format.
  * `--type` (Optional): The case type. Either `Civil` or `Criminal`. Defaults to `Civil`.

-----

### **Step-by-Step Instructions**

1.  **Find the Court Name (If you don't know it):**
    The `--court` argument must be an **exact match**. If you're not sure of the name, run the script with a guess. The script is designed to fail and print a list of all available court names for that complex.

    ```bash
    # This command will fail, but will list the correct court names
    python scrapper.py --complex "Patiala House Court Complex" --court "A guess" --date "19/10/2025"
    ```

    **Output:**

    ```
    --- ERROR: Could not find Court Number ---
    The text 'A guess' was not found in the dropdown.
    ...
    Available court names in the dropdown are:
    - 1 Ms. Anju Bajaj Chandna - Principal District and Sessions Judge
    - 10 Ms. Deepti Devesh - Additional Sessions Judge (SFTC)
    ...
    ```

2.  **Run the Script with the Correct Info:**
    Copy the *exact* court name from the list and use it in your command.

    ```bash
    python scrapper.py --complex "Patiala House Court Complex" --court "1 Ms. Anju Bajaj Chandna - Principal District and Sessions Judge" --date "19/10/2025" --type Civil
    ```

3.  **Solve the CAPTCHA:**
    The script will open Edge, fill the form, and then pause. It will save a `captcha.png` file in the same folder.

      * Look at the `captcha.png` image.
      * Type the text you see into the terminal and press **Enter**.

    <!-- end list -->

    ```
    CAPTCHA image saved as 'captcha.png'.
    Please look at the image and enter the CAPTCHA text: da83a
    ```

4.  **Get Results:**
    If the CAPTCHA is correct and data exists for that day, the script will wait for the results table, print its full contents to the console, and then close the browser.

    ```
    Form submitted. Waiting for results...
    Waiting for results table to load...

    --- Scraping Results ---
    S.NO.
    COURT NAME
    CASE DETAILS
    ...
    (All table data will be printed here)
    ...
    Closing the browser.
    ```
