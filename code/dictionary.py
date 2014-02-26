from nltk_tools import *
import os


def main():
  dictionary = make_dictionary()


def get_dictionary():
  stemmer = NltkTools()
  corpus_dir = os.path.dirname(os.path.abspath(__file__)) + '/../corpus'
  filename = corpus_dir + "/dict.txt"
  return create_dictionary(filename, stemmer)

'''
given a file of the form:
spanish_word: englishWord1, englishWord2...
spanish_word: englishWord1, englishWord2, englishWord3...
returns a dictionary {spanWord -> [engW, engW], spanWord -> [engW, engW,...]}
'''
def create_dictionary(filename, stemmer):
  dictionary = {}
  with open(filename) as f:
    content = f.readlines()
    for line in content:
      split = line.split(":")
      translation_list = []
      for translation in split[1].split(','):
        translation_list.append(translation.strip())
      dictionary[stemmer.stem_spanish_word(split[0].decode('quopri').decode('utf-8'))] = translation_list

  return dictionary




if __name__ == '__main__':
  main()


