import requests
from bs4 import BeautifulSoup
import os
import urllib
 
# The URL to scrape
url = "https://api.python.langchain.com/en/latest/api_reference.html"
 
# The directory to store files in
output_dir = "./langchain-docs/"
 
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
 
# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
 
# Find all links to .html files
links = soup.find_all('a', href=True)
 
for link in links:
    href = link['href']
    
    # If it's a .html file
    if href.endswith('.html'):
        # Make a full URL if necessary
        if not href.startswith('http'):
            href = urllib.parse.urljoin(url, href)
            
        # Fetch the .html file
        file_response = requests.get(href)
        
        # Write it to a file
        file_name = os.path.join(output_dir, os.path.basename(href))
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(file_response.text)

