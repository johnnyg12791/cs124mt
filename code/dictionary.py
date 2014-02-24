from nltk_tools import *


def main():
  stemmer = NltkTools()
  filename = "../corpus/dict.txt"
  print create_dictionary(filename, stemmer)


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
      dictionary[stemmer.stem_word(split[0].decode('quopri').decode('utf-8'))] = translation_list
  return dictionary




if __name__ == '__main__':
  main()


