import sys
import os
import nltk_tools
from dictionary import *
import difflib
import unicodedata

DEV_SET = os.path.dirname(os.path.abspath(__file__)) + '/../corpus/dev_set.txt'
TEST_SET = os.path.dirname(os.path.abspath(__file__)) + '/../corpus/test_set.txt'
DEV_SET_NO_ACCENTS = os.path.dirname(os.path.abspath(__file__)) + '/../corpus/dev_set_unaccented.txt'

SER = {"ser":"to be", "soy":"am", "eres":"are", "es":"is", "somos":"are", "son":"are"}
SER_PAST = {"fui":"was", "fuiste":"was", "fue":"was", "fuimos":"were", "fueron":"were"}

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
  
  # Initialize
  words = sentence.split()
  translated_sentence = ["" for i in range(len(words))]
  
  # These are our rules
  
  # 1 - POS tagging (not technically doing anything)
  pos_words = nltk.spanish_unigram_pos_tag(sentence) 
  #Bug here now (meanings = dictionary[stemmed_word], KeyError: u'a\xf1os')
  #pos_words = update_word_pos_tags(pos_words, dictionary, nltk)
  
  # 2 - check for present progressive (ex. running)
  for index, word in enumerate(words):
    if(translated_sentence[index] == ""):
      (punctuation, word) = get_punctuation(word)
      translated_sentence[index] = check_for_ing(word, dictionary, nltk) + punctuation

  # 3 -loop though and replace ue with o, then add it to translated_sentences[index]
  for index, word_tuple in enumerate(pos_words):
    if(translated_sentence[index] == ""):
      word, pos = word_tuple
      (punctuation, word) = get_punctuation(word)
      if(pos == 'V'):
        translated_sentence[index] = check_for_stem_changing(word, dictionary, nltk) + punctuation


  # 4 - switch (noun adj) -> (adj noun)
  index = 0
  for w1, w2 in zip(pos_words, pos_words[1:]):
    if w1[1] == 'N' and w2[1] == 'A' and translated_sentence[i] == "":
      d1 = get_unigram_word(w1[0], dictionary, nltk)
      d2 = get_unigram_word(w2[0], dictionary, nltk)
      translated_sentence[index] = d2
      translated_sentence[index+1] = d1
    index += 1

  # 5 - verb conjugation??
  for index, word_tuple in enumerate(pos_words):
    if(translated_sentence[index] == ""):
      word, pos = word_tuple
      (punctuation, word) = get_punctuation(word)
      if(pos == 'V'):
        translated_sentence[index] = conjugate_word(word, dictionary, nltk) + punctuation


  # 6 - pluralize words
  for index, word_tuple in enumerate(pos_words):
    if(translated_sentence[index] == ""):
      word, pos = word_tuple
      (punctuation, word) = get_punctuation(word)
      if(pos == 'N'):
        translated_sentence[index] = check_for_plural_word(word, dictionary, nltk) + punctuation

  # 7 - translate remaining words directly using unigram LM
  for index, word in enumerate(words):
    if(translated_sentence[index] == ""):
      (punctuation, word) = get_punctuation(word)
      translated_sentence[index] = get_unigram_word(word, dictionary, nltk) + punctuation

  english_sentence = " ".join(translated_sentence)
  
  # post-processing (ie, alignment, grammar corrections)



  return english_sentence


def check_for_plural_word(word, dictionary, nltk):
  if(word[-1] == "s"):
    definition = get_unigram_word(word, dictionary, nltk)
    if(definition[-1] != "s"):
      if(definition[-1] == "y"):
        return definition[:-1] + "ies"
      else:
        return definition + "s"
    else:
      return definition
  return ""



#given a word, dictionary and nltk, this attempts to conjugate a verb
def conjugate_word(word, dictionary, nltk):
  stemmed_word = nltk.stem_spanish_word(word)
  meaning = get_unigram_word(stemmed_word, dictionary, nltk)
  #Go though various verb subjects/tenses and conjugate definition accordingly
  verb_trans = ""
  if stemmed_word + "o" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:]
    else:
      verb_trans = meaning

  # You
  elif stemmed_word + "as" == word or stemmed_word + "es" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:]
    else:
      verb_trans = meaning

  # He/She/It
  elif stemmed_word + "a" == word or stemmed_word + "e" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "s"
    else:
      verb_trans = meaning

  # We
  elif stemmed_word + "amos" == word or stemmed_word + "emos" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:]
    else:
      verb_trans = meaning

  # They
  elif (stemmed_word + "an" == word and word[:len(word) - 4] != "aban") or stemmed_word + "en" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:]
    else:
      verb_trans = meaning

  # Imperfect tense:
  # I
  elif stemmed_word + "aba" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "ed"
    else:
      verb_trans = meaning
  # You

  elif stemmed_word + "abas" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "ed"
    else:
      verb_trans = meaning

  # He/She/It

  # We

  # They
  elif stemmed_word + "aban" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "ed"
    else:
      verb_trans = meaning

  # PRETERITE
  # I


  # You
  elif stemmed_word + "aste" == word or stemmed_word + "iste" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "ed"
    else:
      verb_trans = meaning

  # He/She/It

  # We
  elif stemmed_word + "amos" == word or stemmed_word + "imos" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "ed"
    else:
      verb_trans = meaning

  # They
  elif stemmed_word + "aron" == word or stemmed_word + "ieron" == word:
    if meaning[:3] == "to ":
      verb_trans = meaning[3:] + "ed"
    else:
      verb_trans = meaning

  return verb_trans



#Some of the tagging (nouns and verbs) was not done correctly, we are manually editing the tags
def update_word_pos_tags(pos_words, dictionary, nltk):
  for i, word_tuple in enumerate(pos_words):
    word, pos = word_tuple
    if pos == None:
      stemmed_word = nltk.stem_spanish_word(word)
      if stemmed_word not in dictionary:
        matches = difflib.get_close_matches(stemmed_word, dictionary.keys())
        if len(matches) != 0:
          stemmed_word = matches[0]
        else:
          stemmed_word = word
      meanings = dictionary[stemmed_word]
      first_meaning = meanings[0]
      tokens = first_meaning.split()
      if len(tokens) > 1 and tokens[0] == "to":
        pos_words[i] = (word, "V")
  #now we also go through the nouns and update thouse
  #for i, word_tuple in enumerate(pos_words):
  #  word, pos = word_tuple
  #  if pos == None:
  #    pos_words[i] = (word, "N")
  return pos_words


#some verbs in spanish are 'stem-changing' where o -> ue and e -> ie in the middle of the verb
def check_for_stem_changing(word, dictionary, nltk):
  if("ue" in word[:-1] and word not in SER_PAST):
    word = word.replace("ue", "o")
    return get_unigram_word(word, dictionary, nltk)
  elif("ie" in word[:-1]):
    word = word.replace("ie", "e")
    return get_unigram_word(word, dictionary, nltk)
  else:
    return ""




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



#return "" if the word isn't -ando, -iendo, english word if it is
def check_for_ing(word, dictionary, nltk):
  if(word[-4:] == 'ando'):
    new_word = word[:-4] + 'ar'
    definition = get_unigram_word(new_word, dictionary, nltk)
    return get_ing(definition)
  elif(word[-5:] == 'iendo'):
    new_word = word[:-5] + 'er'
    definition = get_unigram_word(new_word, dictionary, nltk)
    return get_ing(definition)
  else:
    return ""

#used as a helper function only (for get unigram_word)
def get_most_likely_definition(word, dictionary, nltk):
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



#remove "to " from the definition    
#if the last letter of the english word definition is 'e', we remove it before adding ing
#otherwise just add "ing" and be done
def get_ing(definition):
  if(definition[:3] == 'to '):
    if(definition[-1] == "e"):
      return definition[3:-1] + 'ing'
    else:
      return definition[3:] + 'ing'
  else:
    return definition

# not working...
def convert_string(input):
  unicodedata.normalize('NFKD', unicode(input, 'ISO-8859-1')).encode('ASCII', 'ignore')
    
# A helper function that avoids a lambda function being 
# pickled in the defaultdict (used in loading models)
def _dd():
  return 0

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
