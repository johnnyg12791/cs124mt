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
  #print SpanEngDict.unstemmed_dictionary
  dictionary = SpanEngDict.dictionary
  print "We are translating from Spanish to English."
  with open(DEV_SET) as f:
    content = f.readlines()
    for line in content:
      
      #print "Spanish: ", line
      
      translation = translate(nltk, line, dictionary)
      
      print "English: ", translation
      
      #break


def translate(nltk, sentence, dictionary):
  
  words = sentence.split()
  translated_sentence = ["" for i in range(len(words))]
  pos_words = nltk.spanish_unigram_pos_tag(sentence)

  # ["es", "feliz"]
  # ["he is", "happy"]
  
  #go word by word
  #tag each POS

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

  for word_tuple in pos_words:
    word, pos = word_tuple
    if pos == None:
      stemmed_word = ""
      matches = difflib.get_close_matches(word, dictionary.keys())
      if len(matches) != 0:
        stemmed_word = matches[0]
        meanings = dictionary[stemmed_word]
        first_meaning = meanings[0]
        '''
        tokens = first_meaning.split()
        if len(tokens) > 1 and tokens[0] == "to":
          print meanings
          pos_words[i] = (word, "V")
        '''

  for i, word_tuple in enumerate(pos_words):
    word, pos = word_tuple
    if pos == None:
      pos_words[i] = (word, "N")

  i = 0
  while True:
    word_tuple = pos_words[i]
    word, pos = word_tuple

    # VERBS
    if pos == 'V':
      ser = {"ser":"to be", "soy":"am", "eres":"are", "es":"is", "somos":"are", "son":"are"}
      ser_past = {"fui":"was", "fuiste":"was", "fue":"was", "fuimos":"were", "fueron":"were"}

      if word in ser:
        if i < len(pos_words) - 1 and (pos_words[i + 1][0] == "el" or pos_words[i + 1][0] == "la"):
          translated_sentence[i + 1] = "the"
          i += 1
        translated_sentence[i] = ser[word]
        i += 1
      elif word in ser_past:
        if i < len(pos_words) - 1 and (pos_words[i + 1][0] == "el" or pos_words[i + 1][0] == "la"):
          translated_sentence[i + 1] = "the"
          i += 1
        translated_sentence[i] = ser_past[word]
        i += 1

      else:
        if "ue" in word[:-1]:
          word = word.replace("ue", "o")
        elif "ie" in word[:-1]:
          word = word.replace("ie", "e")
        stemmed_word = nltk.stem_spanish_word(word)
        
        #print stemmed_word, word

        # if dictionary doesn't have stemmed word, then use closest match from dictionary
        meaning = ""
        if stemmed_word not in dictionary:
          matches = difflib.get_close_matches(stemmed_word, dictionary.keys())
          if len(matches) != 0:
            meaning = get_most_likely_definition(nltk, matches[0], dictionary)
          else:
            meaing = word
        else:
          meaning = get_most_likely_definition(nltk, stemmed_word, dictionary)

        tokens = meaning.split()

        #print word
        verb_trans = ""

        #VERB TENSES - Regular:
        # Present tense:
        # I
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

        else:
          print stemmed_word, word

        if verb_trans:
          translated_sentence[i] = verb_trans
        else:
          translated_sentence[i] = meaning
          #print word, translated_sentence[i]
        i += 1

    # OTHER PARTS OF SPEECH
    else:
      i += 1

    if i == len(pos_words):
      break
  return translated_sentence

  #go word by word
  #if word is a verb, try to figure out tense and subject(1st, 2nd, 3rd person)
    #choose most likely meaning based on tri/bigram with stupid backoff
    #look at (verb, next_noun)

  #if the word is a noun (or None), check if it is plural or not
    #choose most likely based on bigram with stupid backoff to unigram
    #(noun, word)

  #if the word is a present tense of 'ser' ie, "es, son..."
    #check if the next word is "el"
      #replace with "is the" "are the" ie, caracas es el capital de venezuela
    #if the next word is not el, and is a ?adjective?
      #replace 'es' with 'it is'

  #for word_index in range(len(sentence)-1):
    #cur_word = sentence[word_index]
    #next_word = sentence[word_index+1]
    #if(cur_word == "es" and next_word == "el"):
      #is the

  #stem changing verbs
  #if there is a verb that has an 'ue', try replacing it with o
  #if there is a verb that has an 'ie', try replacing it with just e
    #check for the new word in the dictionary


  #need to convert verb endings to infinitive, while remembering conjugation
  #then find english translation, and conjugate it in english
  #for word in words:
    #ing_ending = check_for_ing(word, dictionary)



# model definition
# TONIGHT: implement unigram
# NEXT: implement stupid backoff from bigram to unigram (if possible)
def get_most_likely_definition(nltk, spanish_word, dictionary):
  meanings = dictionary[spanish_word]
  first_word = meanings[0]
  
  max_score = nltk.english_unigram_probability(first_word)
  best_meaning = first_word
  
  for meaning in meanings[1:]:
    score = nltk.english_unigram_probability(meaning)
    if score > max_score:
      max_score = score
      best_meaning = meaning
  return best_meaning

  #pass

  #lookup all possible translations in dictionary 
  #possible_translations = dictionary[spanish_word]
  #for word in possible_translations:
    
  #return best_word

def get_most_likely_definition_bigram(nltk, spanish_word_bigram, dictionary):
  pass


#return "" if the word isn't -ando, -iendo, english word if it is
def check_for_ing(word, dictionary):
  #pass
  nltk = NltkTools()
  #if the word ends in "ando" or "iendo", replace it with "ar" or "ir/er"
  if word[-4:] == 'ando':
    new_word = word[:-4] + 'ar'
    definition = get_most_likely_definition(new_word, dictionary)
    
    #check if word[:-4] + ar in dict
      #conjugate + add ing
  #elif word[-5:] == 'iendo':
    #check if word[:-5] + ir in dict
    #check if word[:-5] + er in dict
      #conjugate + add ing
  #else
    #return ""

# A helper function that avoids a lambda function being 
# pickled in the defaultdict (used in loading models)
def _dd():
  return 0

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
