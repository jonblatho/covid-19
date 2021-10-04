import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
from pathlib import Path
from argparse import ArgumentParser

if __name__ == "__main__":
    # Argument parsing setup
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default='~/Downloads', help='The path to the directory where data files should be downloaded. Defaults to ~/Downloads.')
    args = parser.parse_args()

    # Data URLs for the four necessary data tables
    data_urls = {
        "doses": "https://results.mo.gov/t/COVID19/views/COVID-19VaccineDataforDownload/TotalDosesbyCounty?:embed=y&amp;:showVizHome=no&amp;:host_url=https%3A%2F%2Fresults.mo.gov%2F&amp;:embed_code_version=3&amp;:tabs=yes&amp;:toolbar=yes&amp;:showAppBanner=false&amp;:refresh=yes&amp;:display_spinner=no&amp;:loadOrderID=0",
        "initiated": "https://results.mo.gov/t/COVID19/views/COVID-19VaccineDataforDownload/InitiatedVaccinationsbySex?:embed=y&amp;:showVizHome=no&amp;:host_url=https%3A%2F%2Fresults.mo.gov%2F&amp;:embed_code_version=3&amp;:tabs=yes&amp;:toolbar=yes&amp;:showAppBanner=false&amp;:refresh=yes&amp;:display_spinner=no&amp;:loadOrderID=0",
        "completed": "https://results.mo.gov/t/COVID19/views/COVID-19VaccineDataforDownload/CompletedVaccinationsbySex?:embed=y&amp;:showVizHome=no&amp;:host_url=https%3A%2F%2Fresults.mo.gov%2F&amp;:embed_code_version=3&amp;:tabs=yes&amp;:toolbar=yes&amp;:showAppBanner=false&amp;:refresh=yes&amp;:display_spinner=no&amp;:loadOrderID=0",
        "tests": "https://results.mo.gov/t/COVID19/views/COVID-19DataforDownload/MetricsbyTestDatebyCounty?:embed=y&amp;:showVizHome=no&amp;:host_url=https%3A%2F%2Fresults.mo.gov%2F&amp;:embed_code_version=3&amp;:tabs=yes&amp;:toolbar=yes&amp;:showAppBanner=false&amp;:refresh=yes&amp;:display_spinner=no&amp;:loadOrderID=0"
    }

    # Data filenames for the four necessary data tables
    data_filenames = {
        "doses": "Total_Doses_by_County_data.csv",
        "initiated": "Initiated_Vaccinations_by_Sex_data.csv",
        "completed": "Completed_Vaccinations_by_Sex_data.csv",
        "tests": "Metrics_by_Test_Date_by_County_data.csv"
    }

    # Expand the tilde in the supplied path if present
    data_path = args.path
    # If the path includes ~ for the user's home directory, expand it
    if '~' in data_path:
        data_path = os.path.expanduser(data_path)
    # If the default path (or that supplied with --path) doesn't exist, create it
    Path(data_path).mkdir(parents=True, exist_ok=True)

    # Configure some options for headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')

    # Load the page
    for key in ["doses", "initiated", "completed", "tests"]:
        # Set up a headless Chrome driver
        driver = webdriver.Chrome(options=options)
        print(f"Loading table page for {key} view.")
        driver.get(data_urls[key])
        delay = 10

        # Wait for the download button to appear, then simulate clicking on it
        download_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'download-ToolbarButton')))
        print("Download button located. Clicking...")
        download_button.click()
        # Find the download form and data download button, then simulate clicking on the latter
        download_form = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tab-downloadDialog')))
        print("Download form located.")
        download_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@data-tb-test-id='DownloadData-Button']")))
        print("Data download button located. Clicking...")
        download_button.click()

        # Wait a moment to allow a new window to open
        time.sleep(2)

        if len(driver.window_handles) == 1:
            print('New window failed to open. Exiting.')
            exit(1)
        else:
            # Find the new window with the CSV download link
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if 'sessions' in driver.current_url:
                    break

        # We should now be in the window with the data download link.
        print("Successfully switched to data download window. Attempting to find data download link.")
        download_link = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'csvLink_summary')))
        print("Data download link located. Getting URL to download.")
        
        # Download and save the URL.
        download_url = download_link.get_attribute('href')
        save_path = f"{data_path}/{data_filenames[key]}"
        print(f"Saving {download_url} to {save_path} ...")
        request = requests.get(download_url, allow_redirects=True)
        with open(save_path, 'wb') as f:
            f.write(request.content)
        print(f"Saved {save_path}.")

        # Close the file and browser.
        f.close()
        driver.close()