import time
import subprocess
import argparse
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
        chrome_options.add_argument("--disable-application-cache")
        return webdriver.Chrome(options=chrome_options)

    def run_simulation(self):
        """Simulates user interactions with the gallery page."""
        try:
            for i in range(self.iterations):
                print(f"Iteration {i + 1}/{self.iterations}")
                self.driver.get(self.url)

                # Wait for the page to fully load
                time.sleep(1)

                # Scroll all the way to the bottom of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait a moment after scrolling
                time.sleep(1)
        finally:
            self.cleanup()

    def cleanup(self):
        """Closes the WebDriver instance."""
        self.driver.quit()

def main():
    parser = argparse.ArgumentParser(description="Run a Selenium load test after building an application.")
    # parser.add_argument("build_script", help="Path to the build script (e.g., sb-app)")
    parser.add_argument("iterations", type=int, help="Number of times to perform the simulation")
    
    args = parser.parse_args()

    # # Run the build script
    # print(f"Executing build script: {args.build_script}")
    # subprocess.run([f'../{args.build_script}/build.sh'], shell=True, check=True)

    # Define test parameters
    target_url = "http://localhost:8080/gallery"

    # Start load testing
    tester = LoadTester(target_url, args.iterations)
    tester.run_simulation()

if __name__ == '__main__':
    main()
