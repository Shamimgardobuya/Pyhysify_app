import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

main_url =  'https://blog.writefull.com/the-100-most-frequent-latex-commands'
response = requests.get(main_url)

soup = BeautifulSoup(response.text, 'html.parser')
dict_with_values = []
for p in soup.find_all('p'):
    for strong in p.find_all('strong'):
        text = strong.get_text()
        if text.endswith(")"):
            
            ans = p.get_text()    
            dict_with_values.append(ans)
    
