from dictionary import *
import random
from nltk_tools import NltkTools
import string
import re
import os
import translate
import difflib

def main():
  nltk_tools = NltkTools()
  corpus_dir = os.path.dirname(os.path.abspath(__file__)) + '/../corpus'
  dictionary_filename = corpus_dir + "/dict.txt"
  dev_filename = corpus_dir + "/dev_set.txt"

  SpanEngDict = SpanEngDictionary()
  dictionary = SpanEngDict.dictionary
  #dictionary = create_dictionary(dictionary_filename, nltk_tools)
  
  with open(dev_filename) as f:
    content = f.readlines()
    for line in content:
      print unigram_sentences(nltk_tools, dictionary, line)
      print 
      break
'''
  with open(dev_filename) as f:
    content = f.readlines()
    for line in content:
      bigram_sentences(nltk_tools, dictionary, line)
'''


def unigram_sentences(nltk, dictionary, sentence):
  #split sentence into words, while keeping whitespace, to make concatenation easier
  splitter = re.compile(r'(\s+|\S+)')
  words = splitter.findall(sentence)
  
  result = ""
  for word in words:
    #if we only have whitespace, just concatenate
    if word.isspace():
      result += word

    else:
      punc = ""
      #check for punctuation, separatate punctuaion from word
      if (word[len(word) - 1] in string.punctuation):
        punc = word[len(word) - 1]
        word = word[:-1]

      stemmed_word = nltk.stem_spanish_word(word.decode('quopri').decode('utf-8'))
      # if dictionary doesn't have stemmed word, then use closest match from dictionary
      if stemmed_word not in dictionary:
        matches = difflib.get_close_matches(stemmed_word, dictionary.keys())
        if len(matches) != 0:
          result += translate.get_most_likely_definition(nltk, matches[0], dictionary) + punc
        else:
          result += word + punc
      else:
        result += translate.get_most_likely_definition(nltk, stemmed_word, dictionary) + punc
  
  return result


def bigram_sentences(nltk, dictionary, sentence):
  splitter = re.compile(r'(\s+|\S+)')
  words = splitter.findall(sentence)
  result = ""

  # handle first word using unigram
  first_word = words[0]
  first_punc = ""
  if (first_word[len(first_word) - 1] in string.punctuation):
    first_punc = first_word[len(first_word) - 1]
    first_word = first_word[:-1]
  first_stemmed_word = nltk.stem_spanish_word(first_word.decode('quopri').decode('utf-8'))
  if first_stemmed_word not in dictionary:
    result += first_word + first_punc
  else:
    result += get_best_unigram_word(nltk, dictionary[stemmed_word]) + first_punc

  for word in words[1:]:
    punc = ""
    if (word[len(word) - 1] in string.punctuation):
      punc = word[len(word) - 1]
      word = word[:-1]


#helper function
def get_best_unigram_word(nltk, meanings):
  max_score = 0.0
  best_meaning = ""
  for meaning in meanings:
    score = nltk.english_unigram_probability(meaning)
    if score > max_score:
      max_score = score
      best_meaning = meaning
  return best_meaning

# A helper function that avoids a lambda function being 
# pickled in the defaultdict
def _dd():
  return 0


main()