#language models
import collections

def main():
  print build_unigram_model("the world is round")
  print build_bigram_model("the word is round")


def build_unigram_model(corpus):


def build_bigram_model(corpus):
  unigramCounts = collections.defaultdict(lambda: 0)
  for sentence in corpus.corpus:
    for datum in sentence.data:  
      token = datum.word
      unigramCounts[token] = self.unigramCounts[token] + 1
      total += 1
  distinctVocabulary = len(self.unigramCounts)


if __name__ == '__main__':
  main()

