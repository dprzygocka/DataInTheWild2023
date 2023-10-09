import requests
from bs4 import BeautifulSoup
import re
import json
import urllib
import sys

if len(sys.argv) != 2:
    print("Pass the name of the file with songs")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as json_file:
        songs = json.load(json_file)
except FileNotFoundError:
    print(f"Error: The file '{json_file}' does not exist.")
    sys.exit(1)

for song in songs['items']:
    url = 'https://www.tekstowo.pl/piosenka,'
    print(song)
    artist = song['artists'][0].lower().replace(' ', '_').replace('.', '_').replace(')', '_').replace('(', '_')
    artists2 = '_'.join(song['artists']).lower().replace(' ', '_').replace('.', '_').replace(')', '_').replace('(', '_')
    name = re.sub(r'_+', '_', song['name'].lower().replace(' ', '_').replace(',', '').replace('.', '_').replace(')', '_').replace('(', '_')) 
    #case ... is ___ should be _ {'name': 'Seniorita (Gorąca Krew)', 'artists': ['Pezet', 'NOON']} https://www.tekstowo.pl/piosenka,pezet_noon,seniorita_gor%C4%85ca_krew_.html
    #there is this one: {'name': 'Tak Miało Być', 'artists': ['Molesta Ewenement', 'Jamal']} but we are missing feat Jamal
    # {'name': 'Niedopowiedzenia (feat. Pezet)', 'artists': ['Czarny HIFI', 'Pezet']} Pezet in title not as author
    # ___ is not made to _ {'name': 'Nie mamy skrzydeł', 'artists': ['Miuosh']}
    # {'name': 'Fejm', 'artists': ['Rahim', 'Abradab / GrubSon']} artist only Fejm
    # only Peja {'name': 'Mój rap moja rzeczywistość', 'artists': ['Peja', 'Slums Attack']}
    # {'name': 'Nie Odejdę Stąd', 'artists': ['POE (Projekt Ostry Emade)']} (Projekt Ostry Emade) makes it unreadable
    artist_encoded = urllib.parse.quote(artists2)
    name_encoded = urllib.parse.quote(name)
    url = f'{url}{artist_encoded},{name_encoded}.html'
    print(url)

    # Send an HTTP request to the URL
    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        author_title = soup.find("h1", {"class": "strong"}).get_text().split(" - ")
        print(f'Author: {author_title[0]}')
        print(f'Song title: {author_title[1]}')

        #we may require large list that contains words to describe the sections of the text
        pattern = r'(Intro|Verse \d+|Chorus|Ref.:|Outro|Zwrotka \d+|Pre-refren|Refren|Bridge|Przejście|Przed-refren|\[.*?\])'
        text = re.sub(pattern, '', soup.findAll("div", {"class": "inner-text"})[0].get_text(separator="<br/>")).replace("<br/>", '').split('\n')
        filtered_text_list = [item for item in text if item != '' and item != ']' and item != '[' and item != ':']
        #print(f'The song text: {filtered_text_list}')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')