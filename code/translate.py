import sys
DEV_SET = "../corpus/dev_set.txt"
TEST_SET = "../corpus/test_set.txt"
DEV_SET_NO_ACCENTS = "../corpus/dev_set_unaccented.txt"

def main(args):
  print "You are translating from english to spanish"
  with open(DEV_SET) as f:
    content = f.readlines()
    for line in content:
      print "Spanish: ", line
      translation = translate(line)
      print "English: ", translation


def translate(sentence):
  translated_sentence = ""
  #go word by word
  #tag each POS

  #go word by word
  #if word is a verb, try to figure out tense and subject(1st, 2nd, 3rd person)
    #choose most likely meaning based on tri/bigram with stupid backoff
    #look at (verb, next_noun)

  #if the word is a noun, check if it is plural or not
    #choose most likely based on bigram with stupid backoff to unigram
    #(noun, word)

  #if the word is a present tense of 'ser' ie, "es, son..."
    #check if the next word is "el"
      #replace with "is the" "are the" ie, caracas es el capital de venezuela
    #if the next word is not el, and is a ?adjective?
      #replace 'es' with 'it is'

  for word_index in range(len(sentence)-1):
    cur_word = sentence[word_index]
    next_word = sentence[word_index+1]
    if(cur_word == "es"):
      if(next_word == "el" or next_word == "la"):
        translated_sentence += "is the"
    if(cur_word == "son"):
      if(next_word == "los" or next_word == "las"):
        translated_sentence += "are the"



  #if the word is 'el'
    #default to 'the' unless the next word is a verb, then use 'he'
  for word in sentence:
    if word == "el":

  #if the word ends in "ando" or "iendo", replace it with "ar" or "ir/er"
  for word in sentence:
    if word[-4:] == 'ando':
      #check if word[:-4] + ar in dict
        #conjugate + add ing
    if word[-5:] == 'iendo':
      #check if word[:-5] + ir in dict
      #check if word[:-5] + er in dict
        #conjugate + add ing


  return "ENGLISH TRANSLATE" 


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)


