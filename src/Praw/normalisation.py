# import string
# from bs4 import BeautifulSoup
# from nltk import word_tokenize, sent_tokenize
import unicodedata
import re
import inflect
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer  # PorterStemmer
import nltk
import contractions

coin_list = ["bitcoin", "btc", "ethereum", "eth", "ether", "eos", "tether", "usdt", "ripple", "xrp", "litecoin", "ltc", 
"binance", "bnb", "bitcoin-cash", "bch", "libra", "swipe", "sxp", "cardano", "stellar","tron", "cosmos", "dogecoin"]

# these are one time donwloads below
# nltk.download("stopwords")
# nltk.download('punkt')
# nltk.download('wordnet')

def find_coin(words):

    coin_comment = []

    for word in words:
        word = word.lower()

        if word in coin_list:      # is the word a coin
            coin_comment.append(word)
            
    return coin_comment

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

# already called in remove_nouns
def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def replace_contractions(sentence):
    """replace all contractions with full words"""
    
    new_sentence = contractions.fix(sentence)
    
    return new_sentence

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', str(word)) # fix : https://stackoverflow.com/questions/43727583/re-sub-erroring-with-expected-string-or-bytes-like-object
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def remove_nouns(words):
    """Remove nouns from list of tokenized words, this function called once per movie review/comment"""
    
    # allowed_word_types = ["J","R","V"]  # j is adject, r is adverb, and v is verb
    allowed_word_types = ["J"] # this is what python programming allowed for
    new_words = []

    # JJ adjective ‘big’
    # JJR adjective, comparative ‘bigger’
    # JJS adjective, superlative ‘biggest’

    # RB adverb very, silently,
    # RBR adverb, comparative better
    # RBS adverb, superlative best

    # VB verb, base form take
    # VBD verb, past tense took
    # VBG verb, gerund/present participle taking
    # VBN verb, past participle taken
    # VBP verb, sing. present, non-3d take
    # VBZ verb, 3rd person sing. present takes

    POS = nltk.pos_tag(words)           # POS stands for Part of Speech Tagging - returns a list of tuples -> (word, tag)

    for _tuple in POS:
        if _tuple[1][0] in allowed_word_types:      # looks for the first letter in of word tag
            new_words.append(_tuple[0].lower())     # makes word lowercase
    
    return new_words


def stem_words(words):
    """
    Stem words in list of tokenized words
    Stemming reduces inflection in words to their root forms
    Stemming maps a group of words to the same stem even if the
    stem itself is not a valid word in the Language
    """
    # stemmer = PorterStemmer()
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

# this is chunking but I used once ages ago and sacked it, could be useful once i learn how to preoperly use it 
'''
def process_sent_content(tokenizedSent):
    try:
        for sentence in tokenizedSent:
            # check list contains something
            if sentence:
                tagged = nltk.pos_tag(sentence, tagset='universal')

            # <RB.?> --> '.' means any character and combined with '?' for no more than 0 to 1 characters
            # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkGram = r"""Chunk: {<ADJ.?>*<ADV.?>*<VERB.?>*<NOUN>+<NOUN>?}"""
            chunkGramNum = r"""Chunk: {<ADJ.?>*<ADV.?>*<VERB.?>*<NOUN>+<NOUN>?<VERB.?>+<NUM.?>?}"""

            
            #top=ADJ, level=NOUN, comment=NOUN, sometimes upvotes is a VERB or NOUN
            

            chunkParser = nltk.RegexpParser(chunkGramNum)
            chunked = chunkParser.parse(tagged)

            print(chunked)
            # chunked.draw()

    except Exception as e:
        print(str(e))
'''