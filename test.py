# learning playwright
 
from playwright.sync_api import sync_playwright
import time

sample_url = [
    'https://www.justdial.com/',
]

city = 'Ahmedabad' 
query = 'Furniture stores'

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        for url in sample_url:
            page = context.new_page()
            page.goto(url)
            
            page.click('span[aria-label="May be later"]')
            # search for city
            page.query_selector('input.input_location').fill(city)
            search = page.locator('input.input_search')
            time.sleep(2)
            search.fill(query)
        
            page.wait_for_selector()

            time.sleep(15)
            # time.sleep()

 
if __name__ == '__main__':
    main()