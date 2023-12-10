# Data in the Wild
This is a project for course ["Data in the Wild"](https://learnit.itu.dk/course/view.php?id=3022252), given at ITU of Copenhagen during the winter semester of 2023/2024

### Spotify
- Communication with Spotify API defined in [spotify.py](Spotify/spotify.py)  
  - Get full Spotify representation of playlist
  - Get minimal representation of playlist with only song names and artists
  - Get all songs from all the albums from a given artist
  - Helper functions
  - Needs credentials to run (not pushed to GitHub)
- Scraped playlists in [playlists](Spotify/playlists)
- Scraped song names and artists in [songs](Spotify/songs)

### Sentiment 
- Example of using two chained transformers to perform sentiment analysis on Polish song lyrics [sentiment.ipynb](Sentiment/sentiment.ipynb)
  - Translate from Polish to English:  [Helsinki-NLP/opus-mt-pl-en](https://huggingface.co/Helsinki-NLP/)
  - Sentiment analysis: [lxyuan/distilbert-base-multilingual-cased-sentiments-student](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student)
- Sentiment analysis using above transformer to automatically annotate songs chosen for the golden standard [annotate.ipynb](Sentiment/annotate.ipynb)
  - Read all files with song names chosen for golden standard and join them into a single list
  - Read all files with the song lyrics and join them into a single list
  - Annotate songs chosen for the golden standard using transformer, save to json [distilbert.json](Transformation/distilbert.json)


### Transformation
- Text transformation functions defined in [vocabulary.py](Transformation/vocabulary.py)
- Split song lyrics into words: 
    - Remove punctuation
    - Lowerise
    - Return list of words
- Remove stopwords: [Polish](Transformation/polish.stopwords.txt) or [English](Transformation/english.stopwords.txt)
- Count word occurences
    - Sort by frequency, with optional threshold value for minimal frequency of word
    - Sort by alphabetial order, with optional threshold value for minimal frequency of word
    - Create a new word counter from two word counters (example: adding word counters for two songs or albums)
- Transformation, analysis and visualisation of results in [transformation.ipynb](Transformation/transformation.ipynb)
- Read results from the [Excel file](Transformation/golden_standard.xlsx) and transform to dataframe
- Visualise the songs wich were the hardest to annotate manually (sample of 4) [plot](Transformation/plots/annotation_disagreement.png)
- Represent each of the songs that was hard to annotate with words on TF-IDF vs Sentiment [plot](Transformation/plots/sugar-maroon_5.png)
- Sentiment for above words in the plot was taken from the [lexicon](Transformation/vader_lexicon.txt) used by Vader model for sentiment analysis
- Sample of 15 songs was used to visualise annotation choices chosen by humans, Vader model and the Transformer model [plot](Transformation/plots/manual_distilber_vader.png)
- If we assume that manual annotation is our source of truth the Vader model reached **52.94%** of accuracy and Transformer model **72.06%**.

### Tekstowo
- Run parserTekstowo.py by passing the file name with the songs to scrape, i.e.   
```bash
python3 .\Tekstowo\parserTekstowo.py .\Spotify\songs\polski_hip_hop_klasyki_10-03-23.json
```
