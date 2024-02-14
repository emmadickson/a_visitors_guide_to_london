import requests
from bs4 import BeautifulSoup
import subprocess
import wget
import os

def get_soup_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            print(f"Error: Unable to fetch content. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
url_to_scrape = 'https://www.irational.org/heath/london/'
soup = get_soup_from_url(url_to_scrape)

if soup:
    # Now 'soup' contains the BeautifulSoup object, and you can work with it
    for a in soup.find_all('a', href=True):
        if '.gif' in a['href']:
            cmd = [ 'wget', url_to_scrape + a['href'],'-q', '-P images', ] # just download it using wget.
            subprocess.Popen(cmd)
        if '.map' in a['href']:
            cmd = [ 'wget', url_to_scrape + a['href'],'-q', '-P maps', ] # just download it using wget.
            subprocess.Popen(cmd)