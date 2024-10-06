import argparse
import time
import json
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Read Facebook credentials from a file
with open('facebook_credentials.txt') as file:
    EMAIL = file.readline().strip().split('"')[1]
    PASSWORD = file.readline().strip().split('"')[1]

def _login(browser, email, password):
    browser.get("http://facebook.com")
    browser.maximize_window()
    browser.find_element(By.NAME, 'email').send_keys(email)
    browser.find_element(By.NAME, 'pass').send_keys(password)
    browser.find_element(By.NAME, 'login').click()
    time.sleep(5)

def _scroll(browser, num_photos):
    scroll_attempts = 0
    max_attempts = 20
    photos_found = set()

    while scroll_attempts < max_attempts and len(photos_found) < num_photos:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Find all img elements
        img_elements = browser.find_elements(By.TAG_NAME, 'img')
        
        for img in img_elements:
            src = img.get_attribute('src')
            if src and 'scontent' in src and src not in photos_found:
                photos_found.add(src)
                print(f"Found new photo. Total: {len(photos_found)}")

        print(f"Scrolled {scroll_attempts + 1} times. Found {len(photos_found)} unique photos so far.")
        
        if len(photos_found) >= num_photos:
            break

        scroll_attempts += 1

    return list(photos_found)[:num_photos]

def extract(page, num_photos):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=option)
    
    print("Attempting to log in...")
    _login(browser, EMAIL, PASSWORD)
    print("Login attempt completed.")
    
    print(f"Navigating to page: {page}")
    browser.get(page)
    time.sleep(5)  # Wait for the page to load
    
    print(f"Scrolling to find {num_photos} photos...")
    photo_srcs = _scroll(browser, num_photos)
    print("Scrolling completed.")

    photoBigDict = []
    for src in photo_srcs:
        photoDict = {
            'Photo': {
                'src': src,
                'alt': ''  # We don't have alt text in this approach
            },
            'Post': '',
            'Date': ''
        }
        photoBigDict.append(photoDict)

    print(f"Extracted {len(photoBigDict)} photos.")

    browser.quit()  # Use quit() instead of close()

    return photoBigDict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facebook Page Photo Scraper")
    required_parser = parser.add_argument_group("required arguments")
    required_parser.add_argument('-page', '-p', help="The Facebook Public Page you want to scrape", required=True)
    required_parser.add_argument('-len', '-l', help="Number of Photos to extract", type=int, required=True)
    optional_parser = parser.add_argument_group("optional arguments")
    optional_parser.add_argument('-usage', '-u', help="What to do with the data: "
                                                      "Print on Screen (PS), "
                                                      "Write to CSV File (CSV) (Default is CSV)", default="CSV")
    args = parser.parse_args()

    photoBigDict = extract(page=args.page, num_photos=args.len)

    print(f"Number of photos extracted: {len(photoBigDict)}")

    if args.usage == "CSV":
        print("Writing data to CSV...")
        with open('photo_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Photo URL', 'Photo Description', 'Post Text', 'Date'])

            for photo in photoBigDict:
                writer.writerow([
                    photo['Photo']['src'],
                    photo['Photo']['alt'],
                    photo.get('Post', ''),
                    photo.get('Date', '')
                ])
        
        print("CSV writing completed.")

    print("Finished")
