from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- Selenium Configuration ---
# This is the crucial part for running on a server like Render
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensures the browser runs without a GUI
chrome_options.add_argument("--no-sandbox") # Required for running as root in a container
chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
# Some versions of Chrome/ChromeDriver might need the binary location specified.
# Render's buildpack usually handles this automatically.
# chrome_options.binary_location = "/usr/bin/google-chrome"

# --- Flask App ---
app = Flask(__name__)

@app.route('/scrape')
def scrape_title():
    try:
        # Initialize the WebDriver
        # The service object is optional if chromedriver is in the PATH
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the website
        driver.get("https://example.com")
        
        # Get the data you need
        page_title = driver.title
        
        # Close the driver
        driver.quit()
        
        # Return the data as JSON
        return jsonify({"title": page_title})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Gunicorn, the production server Render uses, will run the app
    # This block is mainly for local testing
    app.run(port=5000)