import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class LoadTester:
    def __init__(self, url, iterations):
        self.url = url
        self.iterations = iterations
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """Initialize the Selenium WebDriver with headless Chrome options."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(options=chrome_options)

    def run_simulation(self):
        """Simulates user interactions with the gallery page."""
        try:
            for i in range(self.iterations):
                print(f"Iteration {i + 1}/{self.iterations}")
                self.driver.get(self.url)

                # Wait for the page to fully load
                time.sleep(2)

                # Just for testing
                # images = self.driver.find_elements(By.TAG_NAME, "img")
                # for idx, img in enumerate(images):
                #     print(f"Image {idx + 1}: {img.get_attribute('src')}")

                # Scroll all the way to the bottom of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait a moment after scrolling
                time.sleep(1)
        finally:
            self.cleanup()

    def cleanup(self):
        """Closes the WebDriver instance."""
        self.driver.quit()

if __name__ == '__main__':
    target_url = "http://localhost:8080/gallery"
    num_iterations = 100
    tester = LoadTester(target_url, num_iterations)
    tester.run_simulation()
