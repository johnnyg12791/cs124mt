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
  translated_sentence = ["" for word in sentence.split()]

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
    if(cur_word == "es" and next_word == "el"):
      #is the

  #stem changing verbs
  #if there is a verb that has an 'ue', try replacing it with o
  #if there is a verb that has an 'ie', try replacing it with just e
    #check for the new word in the dictionary


  #need to convert verb endings to infinitive, while remembering conjugation
  #then find english translation, and conjugate it in english


  #if the word ends in "ando" or "iendo", replace it with "ar" or "ir/er"
  for word in sentence:
    if word[-4:] == 'ando':
      #check if word[:-4] + ar in dict
        #conjugate + add ing
    if word[-5:] == 'iendo':
      #check if word[:-5] + ir in dict
      #check if word[:-5] + er in dict
        #conjugate + add ing
        



if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
