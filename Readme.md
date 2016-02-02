## Readme

### Get API_KEY

- [To get the key](http://developer.nytimes.com/docs)
- [Using the interactive api](http://developer.nytimes.com/io-docs)
- [api document](http://developer.nytimes.com/docs/read/article_search_api_v2)

### Install Dependencies.

- pip install beautifulsoup4

### Create an Environment variable using the following command

- **export** *NY_TIMES_API_KEY* = "Your API key"


### Run the script

Script for collecting data from Articles

positional arguments:
  destination           Destination to store the Articles

optional arguments:
  -h, --help            show this help message and exit
  -k N [N ...], --keywords N [N ...]
                        Keywords for fetching the Articles
  -l LIMIT, --limit LIMIT
                        Limit of the number of Articles to be fetched, must be
                        a multiple of 10
  -j JSON, --json JSON  Name of the Json file containing the urls

