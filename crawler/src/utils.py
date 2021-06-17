from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import re

def get_terms(line):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.

    Argument:
    line -- string (text) to be preprocessed

    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    stemming = SnowballStemmer('spanish')
    stops = set(stopwords.words("spanish"))
    ## START CODE
    line = line.lower()  ## Transform in lowercase
    line = re.sub(r'http\S+', '', line)
    line = re.sub(r'&amp', '', line)
    line = re.sub(r'\d+', '', line)
    line = re.sub(r'\W', ' ', line)
    line = line.split()  ## Tokenize the text to get a list of terms
    line = [word for word in line if word not in stops]  ##eliminate the stopwords (HINT: use List Comprehension)
    line = [stemming.stem(word)
            for word in line]  ## perform stemming (HINT: use List Comprehension)
    ## END CODE
    return line