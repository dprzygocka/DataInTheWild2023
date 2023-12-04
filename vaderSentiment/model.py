from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import os
import json

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

modelItems = []
for item in data['item']:
    sentence = item['lyrics']
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sentence)
    rating = 'undecided'
    if vs['compound'] >= 0.05:
        rating = 'positive'
    elif vs['compound'] > -0.05 and vs['compound'] < 0.05:
        rating = 'neutral '
    elif vs['compound'] <= -0.05:
        rating = 'negative'
    modelItem = {
        "name": item['name'],
        "artist": item['artist'],
        "model result": str(vs),
        "rating": rating
    }
    modelItems.append(modelItem)

data = {
    "item": modelItems
}

filename = json_file_path.split('/')[3].split('.')[0]
with open(f'./vaderSentiment/output/model_{filename}.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)