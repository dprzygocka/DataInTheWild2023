import json
import unicodedata
import sys
import os
import requests

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

#saving the artist name and song name in a list 'Djecaci: Noćna pjesma'
songs_list = []
for item in data['items']:
    artist = item['artists'][0]
    songs_list.append(f"{artist}: {item['name']}")

songs_list = [song.replace("đ", "") for song in songs_list]

normal_chars = ['c','c','z','s','d','C','C','Z','D','S']
replacement_chars = ['č','ć','ž','š','đ','Č','Ć','Ž','Đ','Š']

#calls function to replace the Croatian letters 
songs_list = replace_items(songs_list, replacement_chars, normal_chars)
songs_list = ['https://genius.com/' + item.replace(':', '').capitalize().replace('.', '').replace(' ', '-').replace('?', '').replace('!', '').replace(',', '').replace('\'', '').replace("sc", "").replace("cc", "c").replace("dzz", "dz") + '-lyrics' for item in songs_list]



songs_list = replace_combining_charon(songs_list)

final_urls = [url.replace('Kid-rada', 'Kid-raa') for url in songs_list]
final_urls = [url.replace('daku', 'aku') if 'Kid-raa' in url else url for url in final_urls]
final_urls = [url.replace('Marin-ivanovic-stoka', 'stoka') if 'stoka' in url else url for url in final_urls]
final_urls = [url.replace('50-g', '50g') if 'Kreso' in url else url for url in final_urls]
final_urls = [url.replace('Tram-11', 'El-bahattee') if 'Tram-11-981' in url else url for url in final_urls]
final_urls = [url.replace('Ttm', 'Ttm-hrv') if 'Ttm' in url else url for url in final_urls]

count = 0

for url in final_urls:
    try:
        response = requests.get(url)

        if response.status_code == 200:
            count += 1
            print(url)

    except Exception as e:
        print(f"An error occurred: {e}")

print(count) 