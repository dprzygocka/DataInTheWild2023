import requests
from bs4 import BeautifulSoup
import re
import json
import urllib
import sys
from itertools import permutations

if len(sys.argv) != 2:
    print("Pass the name of the file with songs")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as json_file:
        songs = json.load(json_file)
except FileNotFoundError:
    print(f"Error: The file '{json_file}' does not exist.")
    sys.exit(1)

data = {'item': []}
notFoundData = {'item': []}
written = False
for song in songs['items']:
    written = False
    url = 'https://www.tekstowo.pl/piosenka,'
    a = [subitem.lower().replace(' ', '_').replace('.', '_').replace(')', '_').replace('-', '_').replace('(','_').replace('ł', 'L')
     for item in song['artists'] 
     for subitem in item.split(" I ")]

    permutations_list = []

    for r in range(1, len(a) + 1):
        try:
            permutations_list.extend(permutations(a, r))
        except Exception:
            continue

    for perm in permutations_list:
        url = 'https://www.tekstowo.pl/piosenka,'
        if len(perm) > 2:
            continue
        artists = re.sub(r'\s\([^)]*\)', '', "_ ".join(perm))
        name_remove_parentheses = re.sub(r'\s\([^)]*\)', '', song['name'])
        name = re.sub(r'[ .]|_+', '_', name_remove_parentheses).lower().replace(',', '')
        artist_encoded = urllib.parse.quote(artists)
        name_encoded = urllib.parse.quote(name)
        url = f'{url}{artist_encoded},{name_encoded}.html'

        print('url')
        print(url)

        # Send an HTTP request to the URL
        try:
            response = requests.get(url)
        except Exception:
            continue
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            author_title = soup.find("h1", {"class": "strong"}).get_text().split(" - ")

            #we may require large list that contains words to describe the sections of the text
            pattern = r'(Intro|Verse \d+|\d+.|Ref. x\d+ |Ref. x\d+|Chorus|Ref.:|Ref. |Ref.|Outro|Zwrotka \d+|Pre-refren|Refren|Bridge|Przejście|Przed-refren|\[.*?\])'
            text = re.sub(pattern, '', soup.findAll("div", {"class": "inner-text"})[0].get_text(separator="<br/>")).replace("<br/>", '').split('\n')
            filtered_text_list = [item for item in text if item != '' and item != ']' and item != '[' and item != ':']
            data['item'].append({'name': author_title[1], 'artist': author_title[0], 'lyrics': filtered_text_list})
            written = True
            break
        else:
            print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
    if not written:
        notFoundData['item'].append({'name': song['name'], 'artist': song['artists'], 'lyrics': ''})

filename = sys.argv[1].split("\\")[-1]
data['item'].append({'nr of songs from original file': len(songs['items']), 'nr of songs from in current file': len(data['item'])})
notFoundData['item'].append({'nr of songs from original file': len(songs['items']), 'nr of songs from in current file': len(notFoundData['item'])})
with open(f'tekstowo_{filename}', 'w', encoding='utf-8') as json_output_file:
    json.dump(data, json_output_file, ensure_ascii=False, indent=4)
with open(f'missing_tekstowo_{filename}', 'w', encoding='utf-8') as json_output_file:
    json.dump(notFoundData, json_output_file, ensure_ascii=False, indent=4)
print(f"Data written to tekstowo_{filename}")