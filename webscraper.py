"""
AUTHOR: Colin Mckay
DATE: 02/15/2025
PURPOSE: This program is a webscraper using selenium resources to search bing.com,
YouTube.com, spotify.com, etc. It is designed to perform google searches and return
filtered results based on the given links in the domain.
What helped me complete this program: Selenium WebDriver. Chrome WebDriver, Webdriver-Manager, and
the time module to ensure pages load fully complete.
"""

import time  # Import time module for delays
from selenium import webdriver  # Selenium WebDriver for browser automation
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.common.keys import Keys  # For simulating keyboard inputs
from selenium.webdriver.chrome.service import Service  # ChromeDriver service
from webdriver_manager.chrome import ChromeDriverManager  # Manage ChromeDriver installation


# Set up and return Chrome WebDriver
def setup_driver():
    service = Service(ChromeDriverManager().install())  # Install and configure ChromeDriver
    driver = webdriver.Chrome(service=service)  # Start Chrome browser
    driver.get("https://www.bing.com")  # Automatically navigate to Bing
    return driver  # Return driver object


# Perform Bing search and collect results
def bing_search(driver, query):
    driver.get("https://www.bing.com")  # Open Bing search page
    time.sleep(1)  # Wait briefly for page to load

    try:
        search_box = driver.find_element(By.NAME, "q")  # Locate search input field
        search_box.send_keys(query + Keys.RETURN)  # Input query and press Enter
        time.sleep(3)  # Wait for search results to load
    except Exception as e:
        print(f"Error interacting with search box: {e}")  # Print error if search fails
        return []  # Return empty list if error occurs

    results = []  # Initialize list for results
    for result in driver.find_elements(By.CSS_SELECTOR, 'li.b_algo'):  # Loop through results
        try:
            link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')  # Get URL
            title = result.find_element(By.CSS_SELECTOR, 'h2').text  # Get result title
            snippet = result.find_element(By.CSS_SELECTOR, '.b_caption p').text if result.find_elements(By.CSS_SELECTOR,
                                                                                                        '.b_caption p') else ""  # Get snippet if available
            results.append({'title': title, 'link': link, 'snippet': snippet})  # Add result to list
        except Exception as e:
            print(f"Error extracting result details: {e}")  # Print extraction error
    return results  # Return collected results


# Display search results
def display_results(results):
    if not results:
        print("No results found.")  # tell the user if no results
    for idx, result in enumerate(results, 1):  # enumerate results then iterate through them with an index
        print(f"Result {idx}:")  # Print result number
        print(f"Title: {result['title']}")  # Print title
        print(f"Link: {result['link']}")  # Print URL
        print(f"Snippet: {result['snippet']}")  # Print description snippet
        print("-" * 80)  # Print separator line


# Recursive search allowing multiple queries
def recursive_search(driver):
    while True:  # Infinite loop until 'exit' is typed
        search_query = input("Enter your search query (or type 'exit' to quit): ")  # Prompt user for input
        if search_query.lower() == 'exit':  # Check if user wants to exit
            break  # Exit loop
        results = bing_search(driver, search_query)  # Perform Bing search
        display_results(results)  # Show search results


# Main method to run the scraper
def main():
    driver = setup_driver()  # Create browser driver
    try:
        recursive_search(driver)  # Start recursive search
    finally:
        driver.quit()  # Close browser when done


if __name__ == "__main__":  # Entry point for script execution
    main()  # Call main function
