# Defining the Spanish Innovation Ecosystem, Data-driven Analysis from 2018-2021
## _Xavier Amat i García_ , _Supervisor: Manuel Portela_, _Universitat Pompeu Fabra_


## Abstract:
Ecosystems are needed to foster regional innovation. The purpose of this research is to define the composition of the Spanish innovation ecosystem and the relationships between its actors. Taking previous studies as conceptual framework, we define three layers to analyse innovation: Society, Institutions and Investments, Regions. We emphasize the importance of studying social relations in a Society layer . For that, we make a data-driven analysis, using social media data combined with open data. We implement a strategy based on machine learning and spatial analysis that provides updated information on the elements of the ecosystem. The results concluded that this set of actors are attached to the geography and their interactions are indispensable to boost the innovation ecosystem.

## Structure of the repository: 
- Crawler: script to gather Twitter data
    - src: source code
        - listener.py: Twitter crawler given specific users
        - stream_listener.py: Stream Twitter crawler given specific filters (location,language,keywords)
    - data: output folder
- Notebook
    - Results: images and html file containing the visualization
    - data: 
        - geo: geodata, shape files
        - others: Regions, Institutions & Investments data
        - raw_original data: Raw data
        - raw_tweets: Raw tweets
    - images: Photoshop edited, regional geography masks
    - InitExploration.ipynb: Jupyter notebook containing the analysis
- Report

## Features

- NLP analysis
- Network analysis
- Spatial analysis
- Frequency analysis
- Correlation analysis
- Topic modelling and clustering
- ML Classification


## Tech

This repository uses a number of open source projects to work properly:

- [Python] 
    - spaCy: spaCy is a library for advanced Natural Language Processing in Python and Cython. It's built on the very latest research, and was designed from day one to be used in real products.
    - nltk: The Natural Language Toolkit (NLTK) is a Python package for natural language processing.
    - matplotlib: Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
    - seaborn:Seaborn is a library for making statistical graphics in Python. It is built on top of matplotlib and closely integrated with pandas data structures.
    - folium: folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the Leaflet.js library.
    - geopy: geopy is a Python client for several popular geocoding web services.
    - gensim: Gensim is a Python library for topic modelling, document indexing and similarity retrieval with large corpora. Target audience is the natural language processing (NLP) and information retrieval (IR) community.
    - pyLDAvis:Python library for interactive topic model visualization
    - tweepy: An easy-to-use Python library for accessing the Twitter API.

## Installation

The scripts of the repository require Python3 and the configuration of Twitter API credentials. 

More info on how to get the credentials here: https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

Install the dependencies and libraries specified.

For the crawler

```sh
cd crawler
python3 stream_listener.py  #or python3 listener.py
```

For the notebook use Anaconda or Visual Studio Code. Note that there are some cells, which are resource expensive and may need high computing power.


## Development

Want to contribute? Great!

We welcome any type of contributions. We encourage and promote open innovation.

## License

MIT

**Free Software!**