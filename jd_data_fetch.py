 
from playwright.sync_api import sync_playwright
import time
import pandas as pd

sample_url = [
    'https://www.trustpilot.com/',
]

city = 'Ahmedabad' 
query = 'Furniture stores'

def extract_data(card,page):
    """
    Function to extract data from a card.

    Parameter : card (playwright element object) : The card from which data is to be extracted.

    Return : data_dict (dict) : The extracted data from the card.
    """

    # Extracting the data from the card
    store_name = card.query_selector('p.typography_heading-xs__jSwUz')
    store_rating= None
    num_reviews = None
    city = None
    country = None
    store_website = None
    store_phone = None
    store_email = None
    store_address = None
    
    if store_name:
        store_name = store_name.inner_text()

    store_reviews = card.query_selector('p[class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7"]')
    if store_reviews:
        store_reviews = store_reviews.inner_text()

        store_rating = store_reviews.split('|')[0].replace('TrustScore ', '')

        num_reviews = store_reviews.split('|')[1].replace(' reviews', '')

    location = card.query_selector('span[class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_metadataItem__Qn_Q2 styles_location__ILZb0"]')
    if location:
        location = location.inner_text()
        city = location.split(',')[0]
        country = location.split(',')[-1]

    print(store_name, store_rating, num_reviews, city, country)

    # revealing contact information
    button = card.query_selector('button[aria-label="Contact"]')
    if button:
        button.click()

    page.wait_for_selector('div.tooltip_tooltip__9gA3F',timeout=10000)
    store_website = page.query_selector('a[data-website-typography="true"]')
    if store_website:
        store_website = store_website.get_attribute('href')
    store_phone = page.query_selector('a[data-phone-typography="true"]')
    if store_phone:
        store_phone = store_phone.get_attribute('href').replace('tel:', '')
    store_email = page.query_selector('a[data-email-typography="true"]')
    if store_email:
        store_email = store_email.get_attribute('href').replace('mailto:', '')

    store_address = page.query_selector_all('li[class="typography_body-s__aY15Q typography_appearance-default__AAY17 styles_item__3AZ_v"]')[-1].inner_text()

    print(store_website, store_phone, store_email, store_address)
    return {
        'store_name': store_name,
        'store_rating': store_rating,
        'num_reviews': num_reviews,
        'location': city,
        'country': country,
        'store_website': store_website,
        'store_phone': store_phone,
        'store_email': store_email,
        'store_address': store_address
    }


def trustpilot_fetch_detail():
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
        page.goto(sample_url[0])
        
        
        # Waiting for the page to load
        page.wait_for_load_state("domcontentloaded")

        # search category
        search_tag = page.query_selector('input[name="query"]')
        search_tag.fill(query)
        
        page.wait_for_selector('a[href="/categories/furniture_store"]')
        page.query_selector('a[href="/categories/furniture_store"]').click()

        df = []

        for _ in range(1, 20):

            # wait for card to load and print all the cards
            page.wait_for_selector('div[class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"]')
            cards = page.query_selector_all('div[class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"]')
            print(cards)
            for card in cards:
                # extract the card data
                card_data = extract_data(card, page)

                # append the card data to the dataframe
                df.append(card_data)
                print(card_data)
            # extract the entire page data
            # data_dict = extract_data(page)
            page.wait_for_selector('a[aria-label="Next page"]')
            page.query_selector('a[aria-label="Next page"]').click()

            time.sleep(5)

        print(df)
        df = pd.DataFrame(df)
        df.to_csv('trustpilot.csv', index=False)
        
        # Closing the browsing context
        context.close()
    
        # Closing the browsing instance
        browser.close()

if __name__ == "__main__":
    trustpilot_fetch_detail() # calling main function for data fetching