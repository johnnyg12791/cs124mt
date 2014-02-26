from nltk_tools import *
import os


class SpanEngDictionary:

  def __init__(self):
    stemmer = NltkTools()
    corpus_dir = os.path.dirname(os.path.abspath(__file__)) + '/../corpus'
    filename = corpus_dir + "/dict.txt"

    self.dictionary = self.create_dictionary(filename, stemmer)
    self.unstemmed_dictionary = self.create_dictionary(filename, None)


  '''
  given a file of the form:
  spanish_word: englishWord1, englishWord2...
  spanish_word: englishWord1, englishWord2, englishWord3...
  returns a dictionary {spanWord -> [engW, engW], spanWord -> [engW, engW,...]}
  '''

  def create_dictionary(self, filename, stemmer):
    dictionary = {}
    with open(filename) as f:
      content = f.readlines()
      for line in content:
        split = line.split(":")
        translation_list = []
        for translation in split[1].split(','):
          translation_list.append(translation.strip())
        if(stemmer != None):
          dictionary[stemmer.stem_spanish_word(split[0].decode('quopri').decode('utf-8'))] = translation_list
        else:
          dictionary[split[0].decode('quopri').decode('utf-8')] = translation_list

    return dictionary


def _dd():
  return 0

def main():
  #stemmer = NltkTools()
  SpanEngDict = SpanEngDictionary()
  print SpanEngDict.dictionary
  print SpanEngDict.unstemmed_dictionary


if __name__ == '__main__':
  main()


