
import requests 
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://dubai.dubizzle.com/search/?keywords=cars&is_basic_search_widget=1&is_search=1')
soup = BeautifulSoup(res.text, 'html.parser')

head_lines = soup.select('.title')
clean_head_list = []
for line in head_lines:
    clean_head_line = line.getText().strip()
    clean_head_list.append(clean_head_line)
    
print(clean_head_list)

