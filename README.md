# Facebook Pages Photo Scraper

## Overview
This Python script automates the process of extracting photo URLs from a specified Facebook page. It uses Selenium WebDriver to navigate Facebook, log in with provided credentials, and scroll through the page to collect unique photo URLs.

## Features
- Automated login to Facebook
- Scrolling through the specified Facebook page
- Extraction of unique photo URLs
- Configurable number of photos to extract
- Output to CSV file

## Requirements
- Python 3.6+
- Selenium WebDriver
- Chrome WebDriver
- BeautifulSoup4
- webdriver_manager

## Installation
1. Clone this repository or download the script.
2. Install the required Python packages: `pip install selenium beautifulsoup4 webdriver_manager`
3. Ensure you have Google Chrome installed on your system.

## Configuration
1. Adjuist the file named `facebook_credentials.txt`.
2. Add your Facebook login credentials to this file.

## Usage
Run the script from the command line with the following arguments: `python scraper.py -page <facebook_page_url> -len <number_of_photos>`. `-page` or `-p`: The URL of the Facebook page you want to scrape. `-len` or `-l`: The number of photos you want to extract. Optional argument: `-usage` or `-u`: Specify the output format (default is CSV). Example: `python scraper.py -page https://www.facebook.com/profile.php?id=0000000000 -len 20`. This command will attempt to extract 20 photo URLs from the specified Facebook page.

## Output
The script generates a CSV file named `photo_data.csv` in the same directory. This file contains the following columns: Photo URL, Photo Description (currently empty in this version), Post Text (currently empty in this version), Date (currently empty in this version).

## How It Works
1. The script logs into Facebook using the provided credentials. 2. It navigates to the specified Facebook page. 3. The page is scrolled multiple times to load more content. 4. During scrolling, the script collects unique photo URLs. 5. The process continues until the desired number of photos is found or the maximum scroll attempts are reached. 6. Collected data is saved to a CSV file.

## Limitations
- The script currently only extracts photo URLs, not associated text or dates.
- Facebook's structure may change, potentially requiring updates to the script.
- Excessive use may violate Facebook's terms of service.

## Troubleshooting
- If the script fails to log in, check your credentials in `facebook_credentials.txt`.
- Ensure you have a stable internet connection.
- If no photos are found, try increasing the number of scroll attempts in the `_scroll` function.

## Disclaimer
This script is for educational purposes only. Be aware that scraping Facebook may violate their terms of service. Use responsibly and at your own risk.

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](link-to-your-issues-page) if you want to contribute.

## License
[Specify your license here, e.g., MIT, GPL, etc.]