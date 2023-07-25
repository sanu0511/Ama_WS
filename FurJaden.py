import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        product_items = soup.find_all("div", {"data-component-type": "s-search-result"})

        products_data = []
        for item in product_items:
            product_url = item.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style"})["href"]
            product_name = item.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text.strip()
            product_price = item.find("span", {"class": "a-offscreen"}).text.strip()
            product_rating = item.find("span", {"class": "a-icon-alt"})
            if product_rating:
                product_rating = product_rating.text.split()[0]
            else:
                product_rating = None

            product_reviews = item.find("span", {"class": "a-size-base"})
            if product_reviews:
                product_reviews = product_reviews.text.replace(",", "")
            else:
                product_reviews = None

            products_data.append({
                "Product URL": "https://www.amazon.in" + product_url,
                "Product Name": product_name,
                "Product Price": product_price,
                "Rating": product_rating,
                "Number of Reviews": product_reviews
            })

        return products_data
    else:
        print(f"Failed to retrieve data from URL: {url}")
        return None

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
all_products_data = []
for page_num in range(1, 21):
    page_url = base_url + str(page_num)
    products_data = scrape_product_data(page_url)
    if products_data:
        all_products_data.extend(products_data)

df = pd.DataFrame(all_products_data)

df.to_csv("product_data.csv", index=False)

def scrape_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        product_details = {
            # for item in product_items:
                "ASIN": soup.find_all("span", {"class": "a-icon-bold"}),
                "Description": soup.find_all("span", {"class": "a-size-medium a-color-base a-text-normal"}),
                "Product Description": soup.find_all("h2",{"span": "Product description"}),
                "Manufacturer": soup.find_all("span", {"class": "a-text-bold"})
        }

        return product_details
    else:
        print(f"Failed to retrieve data from URL: {url}")
        return None


product_urls = df["Product URL"][:200]  
all_product_details = []
for url in product_urls:
    product_details = scrape_product_details(url)
    if product_details:
        all_product_details.append(product_details)

details_df = pd.DataFrame(all_product_details)

details_df.to_csv("product_details.csv", index=False)
