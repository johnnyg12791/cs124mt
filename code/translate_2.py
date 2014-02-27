import sys
import os
import nltk_tools
from dictionary import *
import difflib

DEV_SET = os.path.dirname(os.path.abspath(__file__)) + '/../corpus/dev_set.txt'
TEST_SET = os.path.dirname(os.path.abspath(__file__)) + '/../corpus/test_set.txt'
DEV_SET_NO_ACCENTS = os.path.dirname(os.path.abspath(__file__)) + '/../corpus/dev_set_unaccented.txt'


def main(args):
  nltk = nltk_tools.NltkTools()
  SpanEngDict = SpanEngDictionary()
  dictionary = SpanEngDict.dictionary

  print "We are translating from Spanish to English."
  with open(DEV_SET) as f:
    content = f.readlines()
    for line in content:
      print "English: ", translate(dictionary, nltk, line)
      raw_input("")

def translate(dictionary, nltk, sentence):
  
  words = sentence.split()
  translated_sentence = ["" for i in range(len(words))]
  pos_words = nltk.spanish_unigram_pos_tag(sentence) 
  
  for index, word in enumerate(words):
    (punctuation, word) = get_punctuation(word)
    translated_sentence[index] = check_for_ing(word, dictionary, nltk) + punctuation

  #these are our rules

  #loop though and replace ue with o, then add it to translated_sentences[index]
  for index, word in enumerate(words):
    if(translated_sentence[index] == ""):

    (punctuation, word) = get_punctuation(word)
    if word.pos = noun and words[index + 1] == adjective:
      translate adjective
      translate noun
      translated_sentence[index] = noun
      translated_sentence[index+1] = adjective

  #other stuff here

  #verb conjugation??

  #
  for index, word in enumerate(words):
    if(translated_sentence[index] == ""):
      (punctuation, word) = get_punctuation(word)
      translated_sentence[index] = get_unigram_word(word, dictionary, nltk) + punctuation

  english_sentence = " ".join(translated_sentence)
  #post-processing (ie, alignment, grammar corrections)


  return english_sentence

#given a stemmed word, it finds the best
def get_unigram_word(word, dictionary, nltk):
  stemmed_word = nltk.stem_spanish_word(word.decode('quopri').decode('utf-8'))
  if stemmed_word not in dictionary:
    matches = difflib.get_close_matches(stemmed_word, dictionary.keys())
    if len(matches) != 0:
      return get_most_likely_definition(matches[0], dictionary, nltk)
    else:
      return word
  else:
    return get_most_likely_definition(stemmed_word, dictionary, nltk)


#given a word, checks if the last character is punctuation
def get_punctuation(word):
  punctuation = ""
  if (word[len(word) - 1] in string.punctuation):
    punc = word[len(word) - 1]
    word = word[:-1]
  return (punctuation, word)



def get_most_likely_definition(word, dictionary, nltk):
  #stemmed_word = nltk.stem_spanish_word(word.decode('quopri').decode('utf-8'))
  meanings = dictionary[word]
  first_word = meanings[0]
  max_score = nltk.english_unigram_probability(first_word)
  best_meaning = first_word
  
  for meaning in meanings[1:]:
    score = nltk.english_unigram_probability(meaning)
    if score > max_score:
      max_score = score
      best_meaning = meaning
  return best_meaning



#return "" if the word isn't -ando, -iendo, english word if it is
def check_for_ing(word, dictionary, nltk):
  print "checking word: " + word
  #pass
  #if the word ends in "ando" or "iendo", replace it with "ar" or "ir/er"
  if(word[-4:] == 'ando'):
    new_word = word[:-4] + 'ar'
    definition = get_unigram_word(new_word, dictionary, nltk)
    if(definition[:3] == 'to '):
      return definition[3:] + 'ing'
    else:
      return definition
  elif(word[-5:] == 'iendo'):
    new_word = word[:-5] + 'er'
    definition = get_unigram_word(new_word, dictionary, nltk)
    if(definition[:3] == 'to '):
      return definition[3:] + 'ing'
    else:
      return definition
  else:
    return ""

# A helper function that avoids a lambda function being 
# pickled in the defaultdict (used in loading models)
def _dd():
  return 0

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
