from dictionary import *
import random
from nltk_tools import NltkTools
import string
import re
import os

def main():
  nltk_tools = NltkTools()
  corpus_dir = os.path.dirname(os.path.abspath(__file__)) + '/../corpus'
  dictionary_filename = corpus_dir + "/dict.txt"
  dev_filename = corpus_dir + "/dev_set.txt"

  dictionary = create_dictionary(dictionary_filename, nltk_tools)
  
  #for key in dictionary:
  #  print key

  with open(dev_filename) as f:
    content = f.readlines()
    for line in content:
      #line2 = line.replace("\'", "")
      #print line2
      print baseline_sentences(nltk_tools, dictionary, line)

def baseline_sentences(nltk, dictionary, sentence):
  #exclude = set(string.punctuation)
  #sentence = ''.join(ch for ch in sentence if ch not in exclude)

  #splitter = re.compile(r"[#(\w+)']+|[.,!?; ]", re.UNICODE)

  splitter = re.compile(r'(\s+|\S+)')
  words = splitter.findall(sentence)
  #print words

  #words = sentence.split()
  result = ""
  
  
  for word in words:
    punc = ""
    if (word[len(word) - 1] in string.punctuation):
      punc = word[len(word) - 1]
      word = word[:-1]
      #print word

    stemmed_word = nltk.stem_spanish_word(word.decode('quopri').decode('utf-8'))
    if stemmed_word not in dictionary:
      result += word + punc
    else:
      meanings = dictionary[stemmed_word]
      result += meanings[random.randint(0,len(meanings) - 1)] + punc
  

  return result


if __name__ == '__main__':
  main()
