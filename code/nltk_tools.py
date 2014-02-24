import pickle
import os
import nltk

'''
A wrapper class provided useful implementations of several NLTK tools.

# Example Input:
from nltk_tools import NltkTools
sentence = "Hola, tengo dos perros."
nltk_tools = NltkTools()
for word in sentence.split():
  print nltk_tools.stem_spanish_word(word)

# Example Output:
hola,
teng
dos
perros.

'''
class NltkTools:

  def __init__(self):
    # Set relative NLTK data path for corpora parsing
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    nltk.data.path.append(cur_dir + '/../corpus')
    self.spanish_stemmer = nltk.SnowballStemmer("spanish")
    self.unigram_tagger = self.load_tagger(cur_dir + '/../corpus/taggers/unigram.pickle', 'unigram')
    self.bigram_tagger = self.load_tagger(cur_dir + '/../corpus/taggers/bigram.pickle', 'bigram')
   
  # Generate unigram and bigram word taggers, reading from 
  # pickled files if they already exist       
  def load_tagger(self, filename, ngram):
    tagger = None
    if os.path.isfile(filename):
      tagger_file = open(filename, 'rb')
      tagger = pickle.load(tagger_file)
      tagger_file.close()
    else:
      tagger_file = open(filename, 'wb')
      cess_sents = nltk.corpus.cess_esp.tagged_sents()
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
    
  def unigram_tag(self, sentence):
    sentence = sentence.split()
    return self.unigram_tagger.tag(sentence)
    
  def bigram_tag(self, sentence):
    sentence = sentence.split()
    return self.bigram_tagger.tag(sentence)
   
  # Returns the part of speech associated with the input word 
  # def find_spanish_pos(self, word):
    # return nltk.pos_tag(word)


# TEST CODE - Please feel free to ignore this for the moment.

# test_sentence = "Hola, me llamo Harley y tengo dos perros."
# test_translation = "Hello, my name is Harley and I have two dogs."
# test_dictionary = {"tener":["to have", "to be"], 
#                    "hola":["hello"], 
#                    "perro":["dog", "bitch"],
#                    "llamarse":["to be called", "to call on oneself"],
#                    "y":["and"],
#                    "dos":["two"]}
                   
# nltk_tools = NltkTools()

# print nltk_tools.unigram_tag(test_sentence)