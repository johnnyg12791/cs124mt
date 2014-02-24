import pickle
import string
import os
import nltk

'''
A wrapper class provided useful implementations of several NLTK tools.

Current tools include:
- Spanish-language word stemmer
- Spanish-language unigram/bigram POS tagger

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
    
  # Given a sentence to translate, this returns the POS
  # for each word based on a unigram language model
  def spanish_unigram_tag(self, sentence):
    sentence = sentence.split()
    return self.unigram_tagger.tag(sentence)
    
  # Given a sentence to translate, this returns the POS
  # for each word based on a unigram language model
  def spanish_bigram_tag(self, sentence):
    sentence = sentence.split()
    return self.bigram_tagger.tag(sentence)
  
  def normalize_word(self, word):
    exclude = set(string.punctuation)
    word = ''.join(ch for ch in word if ch not in exclude)
    return word
    
  def split_and_normalize_sentence(self, sentence):
    return [self.normalize_word(word) for word in nltk.word_tokenize(sentence)]
  
  # Returns the part of speech associated with the input word 
  # def find_spanish_pos(self, word):
    # return nltk.pos_tag(word)


# TEST CODE - Please feel free to ignore this for the moment.

# test_dictionary = {"tener":["to have", "to be"], 
#                    "hola":["hello"], 
#                    "perro":["dog", "bitch"],
#                    "llamarse":["to be called", "to call on oneself"],
#                    "y":["and"],
#                    "dos":["two"]}

# test_sentence = "Hola, me llamo Harley y tengo dos perros."
# test_translation = "Hello, my name is Harley and I have two dogs."
                   
# nltk_tools = NltkTools()
# print nltk_tools.split_and_normalize_sentence(test_sentence)

# print nltk_tools.unigram_tag(test_sentence)