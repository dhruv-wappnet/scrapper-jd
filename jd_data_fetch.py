 
from playwright.sync_api import sync_playwright
import time

sample_url = [
    'https://www.justdial.com/',
]

city = 'Ahmedabad' 
query = 'Furniture stores'


def dca_ca_fetch_detail():
    """
    Function to fetch member details from a website and insert them into the database.

    Parameter : None

    Return : None
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--blink-settings=imagesEnabled=false",
                '--disable-gpu',
                '--disable-extensions',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        ) # Launching a Chromium browser instance


        # Creating a new browsing context
        context = browser.new_context()

        # Opening a new page in the browsing context
        page = context.new_page()

        # Navigating to a specific URL
        page.goto("https://www.rcpsych.ac.uk/members/public-members-list/")
        
        # Waiting for the page to load
        page.wait_for_load_state("domcontentloaded")
        

        

        # Closing the browsing context
        context.close()
    
        # Closing the browsing instance
        browser.close()

if __name__ == "__main__":
    dca_ca_fetch_detail() # calling main function for data fetching