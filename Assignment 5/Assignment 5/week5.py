import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

def scrape_olx_pages(base_url, num_pages):
    page_urls = []

    # Loop over the pages you want to scrape
    for page_num in range(1, num_pages + 1):
        url = f'{base_url}?page={page_num}'
        print(f'Scraping page {page_num}...')
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <a> tags
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                # Check if "storia" is in the URL
                if 'storia' in link:
                    page_urls.append(link)
        else:
            print(f'Failed to retrieve page {page_num}')

    return page_urls

def detect_element(soup, keyword):
    """Finds the tag and class of an element containing a specific keyword (e.g., '€' for price, 'm²' for size)."""
    for tag in ["h3", "strong", "span", "p", "div"]:
        elements = soup.find_all(tag)
        for element in elements:
            if element and keyword in element.text:
                class_name = element.get("class")
                if class_name:
                    return tag, " ".join(class_name)
    return None, None  # If nothing is found


def get_listing_data(url):
    """Extracts rental prices and apartment sizes from a given OLX page dynamically."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Detect price element
    price_tag, price_class = detect_element(soup, "€")
    price = "Price not found"
    if price_tag and price_class:
        price_element = soup.find(price_tag, class_=price_class)
        if price_element:
            price_match = re.search(r'\d+', price_element.text.replace(".", ""))
            if price_match:
                price = price_match.group(0)

    # Size detection
    size = "Size not found"
    size_elements = soup.find_all("div")  # Look in <p> tags first
    for element in size_elements:
        text = element.text.replace(" ", "")  # Remove spaces to match cases like "50m²"
        if "m²" in text:
            size_match = re.search(r'(\d+)(?=m²)', text)  # Extract number before 'm²'
            if size_match:
                size = size_match.group(0)  # Get the size value
            break

    # Rooms detection
    rooms = "Rooms not found"
    rooms_elements = soup.find_all("div")  # Look in <p> tags first
    for element in rooms_elements:
        text = element.text.replace(" ", "")  # Remove spaces to match cases like "50m²"
        if "camere" in text:
            rooms_match = re.search(r'(\d+)(?=camere)', text)  # Extract number before 'm²'
            if rooms_match:
                rooms = rooms_match.group(0)  # Get the size value
            break

    if rooms == "Rooms not found":
        return None

    return {"Price ":price,"Size ":size,"Rooms":rooms}

def scrape_olx(urls):
    """Scrapes data from multiple OLX URLs dynamically."""
    all_data = []

    for url in urls:
        print(f"Scraping data from {url}...")
        data = get_listing_data(url)
        if data:
            all_data.append(data)
        time.sleep(2)  # Delay to prevent being blocked

    return pd.DataFrame(all_data)

# base_url = "https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/cluj-napoca/"
# num_pages = 10
# urls = set(scrape_olx_pages(base_url, num_pages))
#
# # Scrape data
# rental_data = scrape_olx(urls)
#
# # Display results
# print(rental_data)
#
# # Save to CSV
# rental_data.to_csv("olx_rentals.csv", index=False)

data = pd.read_csv("olx_rentals.csv")

prices = np.array(data["Price"].values.tolist())
sizes = np.array(data["Size"].values.tolist())
avg_price = statistics.mean(prices)
#
print(avg_price)

# Visualising the data

# Scatter Plot: Size vs. Price
plt.figure(figsize=(9.5, 6))
sns.scatterplot(x=data["Size"], y=data["Price"], hue=data["Rooms"], palette="coolwarm", s=100)
plt.xlabel("Apartment Size (m²)")
plt.ylabel("Rental Price (€)")
plt.title("Rental Price vs. Apartment Size")
plt.legend(title="Rooms")
plt.grid()

# Caption
plt.subplots_adjust(bottom=0.3)
caption_text = "Fig.1 Distribution of rental prices (€) showing a normal-like frequency pattern. Peak at 500-600 €, with most rentals concentrated between 400-700 €. Slight right skew indicates presence of higher-priced properties. Total sample reveals a typical market pricing structure across 300-1000 € range. The consistent clustering around the 500-600 € range suggests a stable rental market with predictable pricing. The right-side tail implies some premium or luxury rentals exist, potentially reflecting variations in property quality, location, or amenities."
wrapped_caption = textwrap.fill(caption_text, width=120)
plt.text(0.5, -0.2, wrapped_caption, ha='center', va='top', transform=plt.gca().transAxes)

plt.show()


# Box Plot: Price Distribution by Number of Rooms
plt.figure(figsize=(9.5, 7.5))
sns.boxplot(x=data["Rooms"], y=data["Price"], palette="coolwarm")
plt.xlabel("Number of Rooms")
plt.ylabel("Rental Price (€)")
plt.title("Rental Price Distribution by Number of Rooms")
plt.grid()

# Caption
plt.subplots_adjust(bottom=0.3)
caption_text = "Fig.2 The box plot illustrates the rental price distribution across apartments with 2, 3, and 4 rooms. There is a clear progressive increase in rental prices as the number of rooms increases. Two-room apartments show the lowest price range, with the median around 500 euros and a relatively compact distribution. Three-room apartments demonstrate a wider price range, with the median rental price rising to approximately 700 euros. Four-room apartments exhibit the highest and most spread-out price distribution, with the median around 800 euros and notable price variability. The visualization reveals not only the expected price increment with additional rooms but also the increasing price dispersion. Notably, each room category contains outliers, with some two-room and three-room apartments priced significantly higher than their typical range. This suggests that factors beyond room count, such as location, amenities, and apartment condition, substantially influence rental pricing in the market."
wrapped_caption = textwrap.fill(caption_text, width=120)
plt.text(0.5, -0.15, wrapped_caption, ha='center', va='top', transform=plt.gca().transAxes)

plt.show()


# Histogram: Rental Price Distribution
plt.figure(figsize=(9.5, 9))
sns.histplot(data["Price"], bins=5, kde=True, color="blue")
plt.xlabel("Rental Price (€)")
plt.ylabel("Count")
plt.title("Distribution of Rental Prices")
plt.grid()

# Caption
plt.subplots_adjust(bottom=0.3)
caption_text = "Fig.3 The scatter plot illustrates the relationship between apartment size and rental prices, with data points color-coded by the number of rooms (2, 3, and 4). The visualization reveals a generally positive correlation between apartment size and rental price, though with considerable variability. Apartments range from approximately 20 to 100 square meters, with rental prices spanning from around 300 to 1000 euros. Blue points (2-room apartments) are predominantly clustered in the lower left quadrant, indicating smaller sizes and lower rental prices. Gray points (3-room apartments) show more dispersion across the mid-range of sizes and prices. Red points (4-room apartments) tend to appear in the upper and right areas of the plot, suggesting larger sizes and higher rental prices. The plot demonstrates that while apartment size is a significant factor in determining rental price, other variables likely influence pricing. The substantial spread of data points indicates that factors beyond size, such as location, amenities, and apartment condition, play crucial roles in rental pricing dynamics."
wrapped_caption = textwrap.fill(caption_text, width=120)
plt.text(0.5, -0.15, wrapped_caption, ha='center', va='top', transform=plt.gca().transAxes)

plt.show()
