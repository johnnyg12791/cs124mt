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


def translate(line):
  return "ENGLISH TRANSLATE" 




if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
