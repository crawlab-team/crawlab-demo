from crawlab import save_item
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.bing.com/search?q=crawlab')
        page.wait_for_selector('#b_results > li.b_algo')

        for el in page.query_selector_all('#b_results > li.b_algo'):
            title = el.query_selector('.b_title h2 > a').text_content() if el.query_selector('.b_title h2 > a') is not None else ''
            url = el.query_selector('.b_title h2 > a').get_attribute('href') if el.query_selector('.b_title h2 > a') is not None else ''
            abstract = el.query_selector('.b_caption > p').text_content() if el.query_selector('.b_caption > p') is not None else ''
            item = {
                'title': title,
                'url': url,
                'abstract': abstract,
            }
            print(item)
            save_item(item)


if __name__ == '__main__':
    main()
