# Readme

### Get API_KEY from NY Times

- [To get the key](http://developer.nytimes.com/docs)
- [Using the interactive api](http://developer.nytimes.com/io-docs)
- [api document](http://developer.nytimes.com/docs/read/article_search_api_v2)

### Install Dependencies.

- pip install beautifulsoup4
- pip install nltk

- Run the following in python

  \>> import nltk

  \>> nltk.download('all')

### Create an Environment variable using the following command

- **export** *NY_TIMES_API_KEY* = "Your API key"


### Steps for running the code

#### Step1: Generate the input file

There are 3 sources of input which need to be translated to a format the main script uses as input.

1. Input from database
2. Input from a csv file
3. Input from NY Times

##### Source 1: Privacy incidents database

1. Export the most recent data from the database, containing descr and link to a json file and store it as url.json in the url folder.
2. Run the dbtoinput.py script to convert it to the required input format, the output is stored as positive.json in the input folder

##### Source 2: Get input from a CSV

1. The Input file should be in a csv format with no headers and the first 3 columns representing Sr. No., Url and Class respectively
2. Run the csvtojson.py file with filename of the csv as an argument, the output is stored as csvinput.json in the input folder

##### Source 3: Fetch articles from NYtimes

1. Run the geninputNY.py file, run it with -h argument for more help
2. If the keyword is "Security" the output is stored in security.json in the input folder
3. If the keywords are "Computer", "Security" the output is stored in CompSec.json in the input folder

#### Step 2: Run the main script

1. Run the main.py in src folder with the json file generated in the previous step as the input
2. The output is stored in training.csv and test.csv files in the src folder
3. This output is the input for the classifier

### Future work

- Web interface for user to input the url via REST API
- Instead of storing the keywords and files in json, considering put them into a NoSQL DB like MongoDB, for distributed computing... 
- More intelligent choose via two different ways(NYtimes and merely text mining)... We can use text mining as the main decision however using the NYtimes json(more attribute) to revise the decision to get a more accurate result.
- Machine Learning techniques.
- Try with different NLP words. we are now using all words(trimmed). Later we can try with using only nouns, verbs, etc...

For more information check the automation part in [Principedia.pdf](https://github.ncsu.edu/Privacy-database-incidents/incidents-collection/blob/master/Principedia.pdf) 


