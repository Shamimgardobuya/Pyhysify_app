import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

main_url =  'https://blog.writefull.com/the-100-most-frequent-latex-commands'
response = requests.get(main_url)

soup = BeautifulSoup(response.text, 'html.parser')
dict_with_values = []
for p in soup.find_all('p'):
    if '%' not in p.get_text():
        continue
    dict_with_values.append( p.get_text().lower())
    
print(dict_with_values)