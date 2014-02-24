import nltk

'''
A wrapper class provided useful implementations of several NLTK tools.

# Example Input:
sentence = "Hola, tengo dos perros."
nltk_tools = NltkTools()
for word in sentence.split():
  print nltk_tools.stem(word)

# Example Output:
hola,
teng
dos
perros.

'''
class NltkTools:

  def __init__(self):
    self.stemmer = nltk.SnowballStemmer("spanish")
    
  def stem_word(self, word):
    return self.stemmer.stem(word)


# TEST CODE - Please feel free to ignore this for the moment.

# test_sentence = "Hola, me llamo Harley y tengo dos perros."
# test_translation = "Hello, my name is Harley and I have two dogs."
# test_dictionary = {"tener":["to have", "to be"], 
#                    "hola":["hello"], 
#                    "perro":["dog", "bitch"],
#                    "llamarse":["to be called", "to call on oneself"],
#                    "y":["and"],
#                    "dos":["two"]}
                   
# nltk_tools = NLTK()

# for word in test_sentence.split():
#   print nltk_tools.stem_word(word)
