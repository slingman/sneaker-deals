from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_nike_deals():
    url = "https://www.nike.com/w?q=air+max+1"

    # Set up Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless for efficiency
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Allow time for page to load

        deals = []
        product_cards = driver.find_elements(By.CLASS_NAME, "product-card")

        for card in product_cards:
            try:
                # Extract Product Name (with fallback)
                try:
                    product_name = card.find_element(By.CLASS_NAME, "product-card__title").text
                except:
                    product_name = card.find_element(By.CSS_SELECTOR, "[data-testid='product-card__title']").text

                # Extract Product URL
                try:
                    product_url = card.find_element(By.CLASS_NAME, "product-card__link-overlay").get_attribute("href")
                except:
                    product_url = card.find_element(By.CSS_SELECTOR, "[data-testid='product-card__link-overlay']").get_attribute("href")

                # Extract Style ID from URL (last part, e.g. FZ5808-400)
                style_id = product_url.split("/")[-1]
                print(f"✅ Nike Style ID Extracted: {style_id}")

                # Extract Image URL
                try:
                    image_url = card.find_element(By.CLASS_NAME, "product-card__hero-image").get_attribute("src")
                except:
                    image_url = card.find_element(By.CSS_SELECTOR, "img.product-card__hero-image").get_attribute("src")

                # Extract Price Information using the new structure
                # The price container is expected to be like:
                # <div id="price-container" class="...">
                #   <span data-testid="currentPrice-container">$91.97</span>
                #   <span data-testid="initialPrice-container">$140</span>
                #   <span data-testid="OfferPercentage">34% off</span>
                # </div>
                try:
                    sale_price_text = card.find_element(By.CSS_SELECTOR, "span[data-testid='currentPrice-container']").text
                    sale_price = sale_price_text.replace("$", "").strip()
                except Exception as e:
                    sale_price = None

                try:
                    regular_price_text = card.find_element(By.CSS_SELECTOR, "span[data-testid='initialPrice-container']").text
                    regular_price = regular_price_text.replace("$", "").strip()
                except Exception as e:
                    # If the initial price isn't found, assume the sale price is the only price.
                    regular_price = sale_price

                try:
                    discount_percent = card.find_element(By.CSS_SELECTOR, "span[data-testid='OfferPercentage']").text.strip()
                except Exception as e:
                    discount_percent = None

                # Convert price strings to floats if possible.
                try:
                    sale_price = float(sale_price) if sale_price else None
                    regular_price = float(regular_price) if regular_price else None
                except:
                    sale_price, regular_price = None, None

                print(f"🟢 Nike Product Found: {product_name} | Sale Price: {sale_price} | Regular Price: {regular_price} | Style ID: {style_id}")

                deals.append({
                    "store": "Nike",
                    "product_name": product_name,
                    "product_url": product_url,
                    "image_url": image_url,
                    "sale_price": sale_price,
                    "regular_price": regular_price,
                    "discount_percent": discount_percent,
                    "style_id": style_id,
                })

            except Exception as e:
                print(f"⚠️ Skipping a product due to error: {e}")

        return deals

    finally:
        driver.quit()

if __name__ == "__main__":
    deals = get_nike_deals()
    for deal in deals:
        print(deal)
