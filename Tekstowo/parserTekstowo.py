import requests
from bs4 import BeautifulSoup
import re


url = 'https://www.tekstowo.pl/piosenka,kylie_minogue,padam_padam.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    author_title = soup.find("h1", {"class": "strong"}).get_text().split(" - ")
    print(f'Author: {author_title[0]}')
    print(f'Song title: {author_title[1]}')

    #we may require large list that contains words to describe the sections of the text
    pattern = r'(Intro|Verse \d+|Chorus|Ref.:|Outro|Zwrotka \d+|Pre-refren|Refren|Bridge|Przejście|Przed-refren|\[.*?\])'
    text = re.sub(pattern, '', soup.findAll("div", {"class": "inner-text"})[0].get_text(separator="<br/>")).replace("<br/>", '').split('\n')
    filtered_text_list = [item for item in text if item != '' and item != ']' and item != '[' and item != ':']
    print(f'The song text: {filtered_text_list}')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')