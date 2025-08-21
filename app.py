import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- Flask App ---
app = Flask(__name__)

# --- Selenium Configuration ---
def get_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # Recommended for containerized environments
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

@app.route('/')
def index():
    return "API is running! Use the /scrape endpoint."

@app.route('/scrape')
def scrape_data():
    driver = None  # Initialize driver to None
    try:
        driver = get_selenium_driver()
        
        # Navigate to the website
        driver.get("https://quotes.toscrape.com/")
        
        # Get the data you need (example: first quote's text)
        first_quote = driver.find_element("css selector", ".text").text
        
        # Return the data as JSON
        return jsonify({"first_quote": first_quote})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Ensure the driver is always closed
        if driver:
            driver.quit()

if __name__ == '__main__':
    # This block is for local testing; Render will use the Gunicorn CMD from the Dockerfile
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
