import json
import unicodedata
import requests
from bs4 import BeautifulSoup
import re
import sys
import os

def replace_items(strings_list, list1, list2):
    results = []

    for string in strings_list:
        modified_string = []
        for char in string:
            if char in list1:
                index = list1.index(char)
                modified_string.append(list2[index])
            else:
                modified_string.append(char)
        results.append(''.join(modified_string))

    return results

#unicode normalisation for formatiing special diacritic letters
def replace_combining_charon(lst):
    new_list = []
    for s in lst:
        normalized_s = unicodedata.normalize('NFD', s)
        replaced_s = normalized_s.replace("̌", "")
        final_s = unicodedata.normalize('NFC', replaced_s)
        new_list.append(final_s)
    return new_list

def replace_char_at_index(input_string, index, new_char):
    char_list = list(input_string)
    if 0 <= index < len(char_list):
        char_list[index] = new_char

        updated_string = ''.join(char_list)
        return updated_string
    else:
        return "Invalid index"


def replace_last_occurrence(input_string):
    index_list = []
    for index, char in enumerate(input_string):
        if char == '–':
            index_list.append(index)

    if index_list:
        input_string = replace_char_at_index(input_string, index_list[-1], ':')

    return input_string

# loading json file 
if len(sys.argv) != 2:
    print("Pass the name of the file with songs")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.isfile(json_file_path):
    print(f"Error: The file '{json_file_path}' does not exist.")
    sys.exit(1)

try:
    with open(json_file_path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' does not exist.")
    sys.exit(1)


songs_list = []
for item in data['items']:
    artist = item['artists'][0]
    songs_list.append(f"{artist}: {item['name']}")


normal_chars = ['c','c','z','s','d','C','C','Z','D','S']
replacement_chars = ['č','ć','ž','š','đ','Č','Ć','Ž','Đ','Š']

#calls function to replace the Croatian letters 
songs_list = replace_items(songs_list, replacement_chars, normal_chars)
songs_list = ['https://genius.com/' + item.replace(':', '').capitalize().replace('.', '').replace(' ', '-').replace('?', '').replace('!', '').replace(',', '').replace('\'', '').replace("sc", "").replace("cc", "c").replace("dzz", "dz") + '-lyrics' for item in songs_list]

songs_list = replace_combining_charon(songs_list)

#a lot of hardcoding stuff
final_urls = [url.replace('Kid-rada', 'Kid-raa') for url in songs_list]
final_urls = [url for url in final_urls if '-rad-lyrics' not in url]
final_urls = [url for url in final_urls if '-ja-sam-ulica' not in url]
final_urls = [url.replace('50-g', '50g') if 'Kreso' in url else url for url in final_urls]
final_urls = [url.replace('Ttm', 'Ttm-hrv') if 'Ttm' in url else url for url in final_urls]
final_urls = [url.replace('Marin-ivanovic-stoka', 'Stoka') if 'stoka' in url else url for url in final_urls] # 1
final_urls = [url.replace('Shorty-dodi-', 'Shorty-hr-doi-') if 'Shorty' in url else url for url in final_urls] # 2

print(final_urls)

soup_list = []
title_list = []
lyrics_list = []

# EXPECTED ERRORS
http_error = 0
connection_error = 0
timeout_error = 0
request_exception_error = 0

for url in final_urls:
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        soup_list.append(soup)
        title_tag = soup.find('title')
        title = title_tag.string if title_tag else "Title not found"
        title_list.append(title)

        lyrics_divs = soup.find_all('div', {'data-lyrics-container': 'true'})

        lyrics_parts = []
        for div in lyrics_divs:

            part_lyrics = div.get_text(separator='\n', strip=True)


            lyrics_parts.append(part_lyrics)


        lyrics = "\n\n".join(lyrics_parts)

        lyrics_list.append(lyrics)

    except requests.exceptions.HTTPError as errh:
        http_error += 1
    except requests.exceptions.ConnectionError as errc:
        connection_error += 1
    except requests.exceptions.Timeout as errt:
        timeout_error += 1
    except requests.exceptions.RequestException as err:
        request_exception_error += 1

title_list = [title.replace(u'\xa0', ' ')  for title in title_list]
title_list = [item.replace(' Lyrics | Genius Lyrics', '') for item in title_list]
title_list = [replace_last_occurrence(item) for item in title_list]
lyrics_list = [title.replace(u'\xa0', ' ')  for title in lyrics_list]
artists = []
songs = []

for title in title_list:

    parts = [part.strip() for part in title.split(':')]


    if len(parts) == 2:
        artists.append(parts[0])
        songs.append(parts[1])

for i, lyrics in enumerate(lyrics_list):
    lyrics = re.sub(r'\[Tekst pjesme "(.*?)"(?: ft\. .*?)?\]', '', lyrics)
    lyrics_list[i] = lyrics

lyrics_lines_list = []


for lyrics in lyrics_list:
    lines = lyrics.split('\n')
    lyrics_lines_list.append(lines)
cleaned_lyrics_list = []

for lyric in lyrics_lines_list:  
    temp_lyric = []              
    for line in lyric:
        if not re.search(r'\[.*?\]', line):
            temp_lyric.append(line)

    cleaned_lyrics_list.append(temp_lyric)
lyrics_lines_list = cleaned_lyrics_list

items = []

for artist, song, lyrics in zip(artists, songs, lyrics_lines_list):
    item = {
        "name": song,
        "artist": artist,
        "lyrics": lyrics
    }
    items.append(item)

data = {
    "item": items
}

with open('songs1.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f'This garbage has found {len(songs_list) - (http_error + connection_error + timeout_error + request_exception_error)} out of {len(songs_list)} urls') 