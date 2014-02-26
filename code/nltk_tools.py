import os
import collections
import pickle
import string
import math
import nltk

'''
A wrapper class provided useful implementations of several NLTK tools.

Current tools include:
- Spanish-language word stemmer => stem_spanish_word(word)
- Spanish-language unigram POS tagger => spanish_unigram_pos_tag(sentence)
- Spanish-language bigram POS tagger => spanish_bigram_pos_tag(sentence)
- English-language (not yet implemented)
- Sentence/word normalizer (not yet implemented)

'''
class NltkTools:

  def __init__(self):
    # Set relative NLTK data path for corpora parsing
    corpus_dir = os.path.dirname(os.path.abspath(__file__)) + '/../corpus'
    nltk.data.path.append(corpus_dir)
    self.spanish_stemmer = nltk.SnowballStemmer("spanish")
    self.es_unigram_tagger = self._load_tagger(corpus_dir + '/taggers/es_unigram.pickle', 'unigram')
    self.es_bigram_tagger = self._load_tagger(corpus_dir + '/taggers/es_bigram.pickle', 'bigram')
    self.en_unigram_model = self._load_model(corpus_dir + '/models/en_unigram.pickle', 1)
    self.en_bigram_model = self._load_model(corpus_dir + '/models/en_bigram.pickle', 2)
   
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
    
  def _load_model(self, filename, ngram):
    model = None
    if os.path.isfile(filename):
      model_file = open(filename, 'rb')
      model = pickle.load(model_file)
      model_file.close()
    else:
      if ngram == 1:
        model_file = open(filename, 'wb')
        model = collections.defaultdict(_dd)
        for word in nltk.corpus.brown.words():
          model[word.lower()] += 1
        pickle.dump(model, model_file, -1)
        model_file.close()
      #else: 
        #model = nltk.model.ngram.NgramModel(ngram, nltk.corpus.brown.words())
    return model
    
  # Returns a stemmed version of the input Spanish word
  def stem_spanish_word(self, word):
    return self.spanish_stemmer.stem(word)
    
  # Given a sentence to translate, this returns the POS
  # for each word based on a unigram language model
  def spanish_unigram_pos_tag(self, sentence):
    sentence = self.split_and_normalize_sentence(sentence)
    return self.es_unigram_tagger.tag(sentence)
    
  # Given a sentence to translate, this returns the POS
  # for each word based on a bigram language model
  def spanish_bigram_pos_tag(self, sentence):
    sentence = self.split_and_normalize_sentence(sentence)
    return self.es_bigram_tagger.tag(sentence)
    
  # Given a unigram, return the probability of that
  # unigram occuring in the Brown corpus
  def english_unigram_probability(self, unigram):
    return math.log(float(self.en_unigram_model[unigram.lower()])/len(nltk.corpus.brown.words()))
  
  # Given a bigram, return the probability of that
  # bigram occuring in the Brown corpus
  def english_bigram_probability(self, bigram):
    return self.en_bigram_model.logprob(bigram[0], [bigram[1]])

  ###############################################################
  # Everything below this line is not yet finished. DO NOT USE! #
  ###############################################################  

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
  
# A helper function that avoids a lambda function being 
# pickled in the defaultdict
def _dd():
  return 0

##### TEST CODE - Please feel free to ignore this. #####

# test_dictionary = {"tener":["to have", "to be"], 
#                    "hola":["hello"], 
#                    "perro":["dog", "bitch"],
#                    "llamarse":["to be called", "to call on oneself"],
#                    "y":["and"],
#                    "dos":["two"]}

# test_sentence = "Hola, me llamo Harley y tengo dos perros."
# test_translation = "Hello, my name is Harley and I have two dogs."
                   
nltk_tools = NltkTools()
test = ['of', 'off']
print 'of: ' + str(nltk_tools.english_unigram_probability(test[0]))
print 'off: ' + str(nltk_tools.english_unigram_probability(test[1]))