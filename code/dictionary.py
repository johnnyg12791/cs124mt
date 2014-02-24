def main():
  filename = "../corpus/dict.txt"
  print create_dictionary(filename)

def create_dictionary(filename):
  dictionary = {}
  with open(filename) as f:
    content = f.readlines()
    for line in content:
      split = line.split(":")
      translation_list = []
      for translation in split[1].split(','):
        translation_list.append(translation.strip())
      dictionary[split[0]] = translation_list
  return dictionary




if __name__ == '__main__':
  main()


