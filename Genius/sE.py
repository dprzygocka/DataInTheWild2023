import json
import sys
import os
import lyricsgenius
genius = lyricsgenius.Genius('AAK5XN4laZhOOMLke3vRsy9Zfae6dUp528-OjHqiNhrwSjbW6pCPQ_VuvFCPiLL6')
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

items = []
for item in data['items']:
    artistName = item['artists'][0]
    try:
        search = genius.search_song(item['name'], artistName)
        string1 = search.lyrics.lower()
        stirng2 = string1.replace(r"verse |[1|2|3]|chorus|bridge|outro","").replace("[","").replace("]","")
        string3= stirng2.lower().replace(r"instrumental|intro|guitar|solo","")
        string4 = string3.replace("\n"," ").replace(r"[^\w\d'\s]+","").replace("efil ym fo flah","")
        string5 = string4.strip()
        item = {
            "name": item['name'],
            "artist": artistName,
            "lyrics": string5
        }
        items.append(item)
    except Exception:
            continue

data2 = {
    "item": items
}
filename = json_file_path.split('/')[3].split('.')[0]
with open(f'genius_{filename}', 'w', encoding='utf-8') as file:
    json.dump(data2, file, ensure_ascii=False, indent=4)

print(f'Found {len(data2["item"])} out of {len(data["items"])} urls') 