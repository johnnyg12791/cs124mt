import os
import pickle
import string
import nltk

'''
A wrapper class provided useful implementations of several NLTK tools.

Current tools include:
- Spanish-language word stemmer
- Spanish-language unigram/bigram POS tagger
- English-language (not yet implemented)
- Sentence/word normalizer (not yet implemented)

'''
class NltkTools:

  def __init__(self):
    # Set relative NLTK data path for corpora parsing
    corpus_dir = os.path.dirname(os.path.abspath(__file__)) + '/../corpus'
    nltk.data.path.append(corpus_dir)
    self.spanish_stemmer = nltk.SnowballStemmer("spanish")
    self.unigram_tagger = self._load_tagger(corpus_dir + '/taggers/unigram.pickle', 'unigram')
    self.bigram_tagger = self._load_tagger(corpus_dir + '/taggers/bigram.pickle', 'bigram')
   
  # Generate unigram and bigram word taggers, reading from 
  # pickled files if they already exist       
  def _load_tagger(self, filename, ngram):
    tagger = None
    if os.path.isfile(filename):
      tagger_file = open(filename, 'rb')
      tagger = pickle.load(tagger_file)
      tagger_file.close()
    else:
      tagger_file = open(filename, 'wb')
      cess_sents = nltk.corpus.cess_esp.tagged_sents(simplify_tags=True)
      if ngram == 'unigram':
        tagger = nltk.UnigramTagger(cess_sents)
      if ngram == 'bigram':
        train_threshold = int(len(cess_sents)*0.9)
        tagger = nltk.BigramTagger(cess_sents[:train_threshold])
        tagger.evaluate(cess_sents[train_threshold:])
      pickle.dump(tagger, tagger_file, -1)
      tagger_file.close()
    return tagger
      
    
  # Returns a stemmed version of the input Spanish word
  def stem_spanish_word(self, word):
    return self.spanish_stemmer.stem(word)
    
  # Given a sentence to translate, this returns the POS
  # for each word based on a unigram language model
  def spanish_unigram_pos_tag(self, sentence):
    sentence = self.split_and_normalize_sentence(sentence)
    return self.unigram_tagger.tag(sentence)
    
  # Given a sentence to translate, this returns the POS
  # for each word based on a bigram language model
  def spanish_bigram_pos_tag(self, sentence):
    sentence = self.split_and_normalize_sentence(sentence)
    return self.bigram_tagger.tag(sentence)
  
  ###############################################################
  # Everything below this line is not yet finished. DO NOT USE! #
  ###############################################################
    
  # Given a unigram, return the probability of that
  # unigram occuring in the Brown corpus
  def english_unigram_probability(self, unigram):
    pass
  
  # Given a bigram, return the probability of that
  # bigram occuring in the Brown corpus
  def english_bigram_probability(self, bigram):
    pass
  
  def normalize_word(self, word):
    exclude = set(string.punctuation)
    word = ''.join(ch for ch in word if ch not in exclude)
    return word.decode('quopri').decode('utf-8').lower()
    
  def split_and_normalize_sentence(self, sentence):
    result = []
    for word in sentence.split():
      if self.normalize_word(word) != '':
        result.append(self.normalize_word(word))
    return result
  

##### TEST CODE - Please feel free to ignore this. #####

# test_dictionary = {"tener":["to have", "to be"], 
#                    "hola":["hello"], 
#                    "perro":["dog", "bitch"],
#                    "llamarse":["to be called", "to call on oneself"],
#                    "y":["and"],
#                    "dos":["two"]}

# test_sentence = "Hóla, me llamo Harley y tengo dos perros."
# test_translation = "Hello, my name is Harley and I have two dogs."
                   
#nltk_tools = NltkTools()
# print nltk_tools.split_and_normalize_sentence(test_sentence)

# print nltk_tools.spanish_unigram_pos_tag(test_sentence)