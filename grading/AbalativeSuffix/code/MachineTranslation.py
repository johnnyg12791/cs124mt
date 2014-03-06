#!/usr/bin/python
# -*- coding: utf-8 -*-
# CS124 Homework 6 Final Project Machine Translation 
# Translation strategies discussed with Natalia Silveira and Dan Jurafsky

import collections
import operator
import nltk
from nltk.tag.stanford import POSTagger
from nltk.corpus import webtext

def generateTranslation(master, english_unigram_model, filename, baseline_ON):
	#If baseline_ON is True, then generate baseline
	#If baseline_ON if False, then generate sentences based on unigram frequency
	"""
  	* Code generates translation given list of chinese sentences (from filename)
  	"""
	source = readFile(filename)
	for sentence in source:
		english = u''
		print sentence.strip('\n')
		sentence = sentence.split(' ')
		for token in sentence:
			if (token != '\n'):
				candidates = generate_candidates(token, master) 
				if baseline_ON == True:
					english += candidates.pop() + ' ' ## (1) JUST BASELINE
				else: 
					english += rankCandidates(english_unigram_model, candidates) + ' ' ## (2) FREQUENCY
		print english

def generateWithPOS(master, english_unigram_model, filename):
	"""
  	* Code generates translation, now with POS tagging enabled
  	"""
	source = readFile(filename)

	for sentence in source:
		english = u''
		print sentence.strip('\n')
		processed_sentence = POSTagging(sentence, False)

		for token_tuple in processed_sentence:
			POS = choosePOS(token_tuple[1])
			word = token_tuple[0]
			word = word.decode('utf-8')
			word = u''+ word
			potentials = master[word] 			
			if POS in potentials:
				translation = master[word][POS]
				candidates = translation
				english += rankCandidates(english_unigram_model, candidates) + ' '
			else:
				candidates = generate_candidates(token_tuple[0], master) 
				english += rankCandidates(english_unigram_model, candidates) + ' '
		print english

def generateFinalTranslations(master, english_unigram_model, filename):
	"""
  	* Code generates final translation, with processing of measurement words, DE, and 
  	special rules for dealing with chinese tokens 要,就,也,有 
  	"""
	source = readFile(filename)

	for sentence in source:
		english = u''
		print sentence.strip('\n')
		processed_sentence = POSTagging(sentence, True)
		analyzed_sentence = analyzePOSTags(processed_sentence)

		for token_tuple in processed_sentence:
			POS = choosePOS(token_tuple[1])
			word = token_tuple[0]
			word = word.decode('utf-8')
			word = u''+ word
			if word == 'SPECIAL_JIO' or word == 'SPECIAL_QU':
				english += 'to '
			elif word == 'SPECIAL_YAO':
				english += 'must '
			elif word == 'SPECIAL_YO':
				english += 'there is '
			elif word == 'SPECIAL_YEI':
				english += 'and '
			else: 
				potentials = master[word] 			
				if POS in potentials:
					translation = master[word][POS]
					candidates = translation
					english += rankCandidates(english_unigram_model, candidates) + ' '

				else:
					candidates = generate_candidates(token_tuple[0], master) 
					english += rankCandidates(english_unigram_model, candidates) + ' '

		english_processed = english_POSTagging(english)
		end_sentence = analyzePOSTags_ENGLISH(english_processed)

		result = ''
		for token in end_sentence:
			if token[1] == 'SPECIAL_POSS':
				result += poss_pronoun_dict[token[0]] + ' '
			else:
				result += token[0] + ' '
		print result


def trainUnigrams():
	"""
  	* Code builds the unigram count model from two sources: gutenberg_childrens_stories and webtext
  	"""
	english_unigrams = collections.defaultdict(lambda: 0)
 	f = open('../gutenberg_childrens_stories') ##(1)Corpus from the given filename
  	for line in f:
  		line = line.split()
  		for token in line:
  			english_unigrams[token] += 1

  	for word in webtext.words():  ##(2)Corpus from nltk webtext
		english_unigrams[word] += 1

	##(3) Unigram Model uses corpus from a combination of (1) and (2)
  	return english_unigrams

def rankCandidates(english_unigram_model, candidates_list):
	"""
  	* Code takes in a list of possible candidates and rank them based on their frequency counts from given english unigram model
  	"""
	ranking = {}
	for candidate in candidates_list:
		ranking[candidate] = english_unigram_model[candidate]

	sort_ranking = sorted(ranking.iteritems(), key=operator.itemgetter(1))
	top_choice = sort_ranking[len(sort_ranking)-1]
	return top_choice[0]

def generate_candidates(chinese_token, master):
	"""
  	* Code generates a list of possible candidate words from master dictionary 
  	based on given chinese_token key
  	"""
	candidates = []
	possibilities = master[chinese_token.decode('utf-8')]
	if type(possibilities) == list:
		candidates += possibilities
	if type(possibilities) == dict:
		for key in possibilities:
			candidates += possibilities[key]
	return set(candidates)


def readFile(filename):
  	"""
  	* Code used for reading chinese source file.
  	"""
  	contents = []
  	f = open(filename)
  	for line in f:
  		line.strip('\n')
  		# unicode_string = line.decode('utf-8')
  		# print unicode_string.encode('utf-8')
   		contents.append(line)
  	f.close()
  	return contents


def POSTagging(sentence, finalTranslation_ON):
	tagger = POSTagger('chinese-distsim.tagger', 'stanford-postagger.jar')
	tagged = tagger.tag(sentence.split())
	processed = extractPOS(tagged, finalTranslation_ON)
	return processed	

def english_POSTagging(english_sentence):
	e_tagger = POSTagger('english-bidirectional-distsim.tagger', 'stanford-postagger.jar')
	e_tagged = e_tagger.tag(english_sentence.split())
	return e_tagged

def analyzePOSTags(sentence):
	verb_prior = False
	word_jio_index = len(sentence)
	word_yao_index = len(sentence)
	word_qu_index = len(sentence)

	for i in xrange(len(sentence)):
		if sentence[i][1].find('#V') > -1 and sentence[i][0] != '就' and i < word_jio_index:
			verb_prior = True
			# print "VERB PRIOR: TRUE", sentence[i][0]

		if sentence[i][0] == '就':
			word_jio_index = i
			# print "FOUND JIO", sentence[i][0]

		if sentence[i][0] == '要':
			word_yao_index = i

		if sentence[i][0] == '去':
			word_qu_index = i

		if sentence[i][0] == '有' and sentence[i-1][1].find('AD') == -1:
			sentence.pop(i)
			new_word = 'SPECIAL_YO'
			new_tag = ''
			sentence.insert(i, (new_word, new_tag))	

		if sentence[i][0] == '也' and sentence[i-1][1].find('PU') > -1:
			sentence.pop(i)
			new_word = 'SPECIAL_YEI'
			new_tag = ''
			sentence.insert(i, (new_word, new_tag))	

		if word_jio_index < len(sentence) and sentence[i][1].find('#V') > -1 and verb_prior == True:
			sentence.pop(word_jio_index)
			new_word = 'SPECIAL_JIO'
			new_tag = ''
			sentence.insert(word_jio_index, (new_word, new_tag))			


		if word_yao_index < len(sentence) and sentence[i][1].find('#V') > -1:
			sentence.pop(word_yao_index)
			new_word = 'SPECIAL_YAO'
			new_tag = ''
			sentence.insert(word_yao_index, (new_word, new_tag))	
		
		if word_qu_index < len(sentence) and sentence[i][1].find('#V') > -1:
			sentence.pop(word_qu_index)
			new_word = 'SPECIAL_QU'
			new_tag = ''
			sentence.insert(word_qu_index, (new_word, new_tag))		

	return sentence


def analyzePOSTags_ENGLISH(english_tagged_sentence):
	sentence = english_tagged_sentence

	for i in xrange(len(english_tagged_sentence)-1):
		if sentence[i][1].find('PRP') > -1 and sentence[i][1].find('PRP$') == -1 and sentence[i+1][1].find('NN') > -1:
			new_word = sentence[i][0]
			new_tag = 'SPECIAL_POSS'
			sentence.pop(i)

			sentence.insert(i, (new_word, new_tag))
	return sentence



def extractPOS(tagged_sentence, finalTranslation_ON):
	"""
  	* Code used extracting specific POS tags such as #DE variants and #M (measurement words)
  	"""
	processed_sentence = []
	for tagged_token in tagged_sentence:
		x = tagged_token[1]
		POS_Index = x.find('#')
		word = x[:POS_Index]
		POS = x[POS_Index:]

		if (finalTranslation_ON):
			if (POS == '#M'):
				if (word == '月' or word == '日' or word == '年' or  word == '夜' or  word == '時' or word == '分' or word == '天'):  #measurement word but followed by a word that signifies time, keep
					processed_sentence.append((word, POS))

			elif ((POS != '#DEC' and POS != '#DEG' and POS != '#DEV' and POS != '#DER') and 
				#DEC:Norminalizer 
				#DEV:Rare case
				#DER:follow verb
				#DEG:possessive
				##The tagger used are mislabeling the DE in our devset, we decide to simply throw away
				(POS != '#M') and
				(word != '了' and word != '吧' and word != '呢' and word != '呀' and word != '喔')): #get rid of words that don't have specific meanings
					processed_sentence.append((word, POS))
		else:
			processed_sentence.append((word, POS))
	return processed_sentence


def choosePOS(POS_tag):
	"""
  	* Code used for translating POSTagger labels to equivalent names in bilingual dictionary
  	"""
	if (POS_tag == '#VA' or POS_tag == '#VC' or POS_tag == '#VE' or POS_tag == '#VV'):
		return 'verb'
	if (POS_tag == '#NR' or POS_tag == '#NT' or POS_tag == '#NN'):
		return 'noun'
	if (POS_tag == '#LC'):
		return 'localizer'
	if (POS_tag == '#PN'):
		return 'pronoun'
	if (POS_tag == '#DT' or POS_tag == '#CD' or POS_tag == '#OD'):
		return 'determiner'
	if (POS_tag == '#M'):
		return 'measure'
	if (POS_tag == '#AD'):
		return 'adverb'
	if (POS_tag == '#P'):
		return 'preposition'
	if (POS_tag == '#CC' or POS_tag == 'CS'):
		return 'conjunction'
	if (POS_tag == 'AS' or POS_tag == 'SP' or POS_tag == 'ETC' or POS_tag == 'MSP'):
		return 'particle'
	if (POS_tag == '#PU'):
		return 'punctuation'


###Helper Functions###
def readFile(filename):
  	"""
  	* Code used for reading chinese source file.
  	"""
  	contents = []
  	f = open(filename)
  	for line in f:
  		line.strip('\n')
  		# unicode_string = line.decode('utf-8')
  		# print unicode_string.encode('utf-8')
   		contents.append(line)
  	f.close()
  	return contents

def printSentence(sentence):
	for word, tag in sentence:
		print ('(' + word + ', ' + tag + ')'),

def printDictionary(dictionary):
	for key, value in dictionary.iteritems():
		if (1 == 1):
			if type(value) == list:
				print (key.encode('utf-8') + ": " + str(value))
			if type(value) == dict:
				print (key.encode('utf-8') + ": "),
				for subkey, subvalue in value.iteritems():
					print (subkey + ": "  + str(subvalue)),
				print '' 

###Dictionary Structures###
bilingual_dict = {	u'她': {'pronoun': ['she']},
				u'沒': {'adverb':['not'], 'verb': ['have not', 'disappear', 'die', 'sink', 'submerge', 'overflow', 'hide'], 'adjective': ['drowned'], 'prefix': ['un-'], 'abbreviation': ['haven\'t']}, 
				u'有': {'verb': ['have', 'be', 'exist']}, 
				u'資格': {'noun': ['qualifications']}, 
				u'未': {'adverb': ['not', 'not yet'], 'verb': ['have not'], 'abbrevitaion':['1-3 p.m.', 'haven\'t']}, 
		 		u'經': {'preposition': ['through', 'after', 'after'], 'noun':['warp', 'channel', 'deformation'], 'verb':['pass through', 'manage', 'endure', 'bear', 'stand'], 'adjective': ['regular', 'abiding', 'changeless', 'immanent', 'ordinate', 'constant', 'scheduled']}, 
				u'家': {'noun': ['home','family','household','specialist','school', 'school of thought'], 'adjective':['domesticated'], 'suffix':['-er','-ian','-ist']},  
				u'屬': {'verb': ['belong', 'enjoin', 'obey', 'submit'], 'adjective': ['dependent', 'subordinate', 'within the jurisdiction'], 'noun': ['subordination', 'kind', 'sort', 'dependency', 'dependence', 'subjection', 'submission']},  
				u'同意': {'verb':['agree', 'concur', 'consent', 'approve' 'assent'], 'noun':['consent', 'assent']}, 
				u'就': {'preposition':['on', 'concerning'], 'adverb':['then', 'with regard', 'already', 'only', 'at once', 'right away', 'right off'], 'conjunction': ['that', 'as soon as', 'as early as'], 'verb':['underdake', 'move towards', 'approach', 'enter']},  
				u'做': {'verb':['do', 'make', 'be', 'act', 'become', 'prepare', 'make out', 'be used as', 'hold a family celebration', 'perpetrate', 'produce', 'compose', 'form a relationship', 'manufacture']}, 
				u'這些': {'pronoun': ['these']},  
				u'事情': {'noun':['thing' ,'matter', 'affair', 'business']},
				u'。': {'punctuation': ['.']},
				u'我':{'pronoun': ['I', 'me', 'myself']}, 
				u'正在': {'conjunction':['while'], 'preposition':['in the process of']}, 
				u'努力': {'verb': ['strive', 'try hard'], 'noun':['great effort', 'exertion','intension']}, 
				u'找': {'verb':['look for', 'seek', 'call', 'approach', 'ask for', 'try to find','want to see']}, 
				u'親戚': {'noun': ['relative', 'cognate']}, 
				u'朋友': {'noun': ['friend', 'pal', 'partner', 'fellow', 'comrade', 'companion', 'boyfriend', 'amigo', 'matey', 'compadre', 'bo', 'cobber']}, 
				u'願意': {'adjective': ['willing', 'ready'], 'verb':['want', 'wish']},  
				u'以': {'preposition': ['with', 'by', 'according to'], 'adverb':['in order to'], 'conjunction': ['so as to', 'because'], 'verb':['use']},  
				u'投資': {'noun':['investment', 'money invested'], 'verb':['invest', 'fund'], 'adjective':['invested']}, 
				u'目的': {'noun': ['purpose', 'aim','intent','object','objective','target','goal']},  
				u'購買': {'noun': ['buy', 'detriment'], 'adjective':['purchasing']}, 
				u'，': {'punctuation': [',']},  
				u'則': {'adverb':['then'], 'noun':['rule', 'regulation', 'criterion', 'standard', 'norm'], 'verb':['follow']}, 
				u'你': {'pronoun': ['you']}, 
				u'仍然': {'adjective': ['still'], 'adverb': ['yet']},  
				u'可以': {'verb':['can', 'may', 'be able to'], 'adjective':['possible']}, 
				u'繼續': {'verb':['continue', 'keep on', 'proceed', 'go on', 'carry on', 'hold on', 'endure'], 'noun':['continuance']}, 
				u'住': {'verb':['live', 'dwell', 'reside', 'stop', 'bide', 'fare']}, 
				u'下去': {'verb': ['go on', 'continue', 'go down', 'descend']},
				u'新年':{'noun': ['New Year']}, 
				u'後': {'adverb': ['after', 'later', 'afterwards', 'afterward']}, 
				u'的': {'preposition': ['of'], 'noun': ['aim'], 'adverb': ['really and truly'], 'particle': ['possessive particle'], 'auxiliary verb': ['ablative cause suffix'], 'suffix': ['-self']}, 
				u'第四': {'adjective':['fourth', 'fourth number']}, 
				u'天': {'noun': ['day','sky','heavens','God','weather','nature','season'], 'adverb':['overhead']}, 
				u'一切': {'noun': ['all'], 'pronoun':['everything'], 'adjective':['every']}, 
				u'生活': {'noun': ['life', 'livelihood', 'activity'], 'verb': ['live', 'get along', 'get on']},  
				u'復常': ['normalization'], 
				u'此': {'pronoun': ['this', 'these'], 'adverb':['here', 'now']}, 
				u'時': {'noun': ['time', 'hour', 'times', 'tense', 'fixed time', 'season', 'chance', 'opportunity'], 'adverb':['from time to time', 'occasionally', 'now and then']},  
				u'能': {'verb': ['can', 'may'], 'adjective':['able', 'capable'], 'noun':['energy', 'ability', 'capability']}, 
				u'外出': ['out'],  
				u'訪友': ['friends'], 
				u'了': {'verb':['know', 'understand', 'finish', 'settle', 'dispose of', 'look afar from a high place'], 'adjective': ['clear'], 'auxiliary verb': ['past tense marker']},
				u'其實':{'adverb': ['in fact', 'as a matter of fact', 'actually', 'really']}, 
				u'最': {'adjective': ['most', 'bottom'], 'suffix': ['-est']}, 
				u'好': {'adjective': ['good'], 'adverb':['well', 'OK', 'fine', 'okay', 'okey', 'okey dokey'], 'verb': ['love', 'like']}, 
				u'實驗對': ['experiment'], 
				u'象': {'noun': ['elephant', 'appearance', 'shape', 'jumbo'], 'verb':['resemble', 'seek', 'take after']}, 
				u'應該': {'auxiliary verb':['should', 'out to'], 'verb':['must']},  
				u'是': {'auxiliary verb': ['be'], 'verb': ['be', 'exist'], 'adjective':['right', 'correct']},  
				u'黑猩猩': {'noun':['chimpanzee', 'chimp', 'jocko']},
				u'東方人':{'noun': ['eastern']}, 
				u'眼睛': {'noun':['eye']}, 
				u'可以': {'verb': ['can', 'may', 'be able to'], 'adjective':['possible']}, 
				u'很': {'adverb': ['very', 'quite', 'extremely', 'passing', 'strongly', 'strong', 'mighty', 'biggerly', 'spanking', 'parlous']}, 
				u'分明': {'adjective': ['distinct', 'clear', 'demarcative'], 'adverb':['clearly', 'obviously', 'evidently', 'plainly']}, 
				u'地': {'noun': ['ground', 'land', 'earth', 'place', 'field'], 'adjective':['topographic', 'topographical'], 'particle':['adverbial particle']},  
				u'看出': {'verb': ['see', 'find out', 'perceive', 'espy']},  
				u'有': {'verb':['have', 'be', 'exist']}, 
				u'黑色': {'noun': ['black', 'blackness', 'dark']},  
				u'眼珠': ['eye'],  
				u'和': {'conjunction':['and'], 'noun':['sum', 'summation', 'peace'], 'adverb':['together'], 'verb':['mix', 'blend', 'draw', 'tie', 'chime in', 'compose a poem in reply', 'join in the singing', 'write a poem in reply'], 'adjective': ['harmonious', 'kind']}, 
				u'白色': {'adjective': ['white'], 'noun': ['white']},
				u'窗': {'noun': ['window', 'shutter']}, 
				u'臺': {'noun': ['station', 'desk', 'platform', 'stage', 'broadcasting station'], 'auxiliary verb': ['measure word for performances']}, 
				u'上': {'preposition': ['on', 'above', 'on top of', 'upon'], 'adjective':['upper', 'last', 'previous','preceding','superior'], 'adverb':['up'], 'verb':['go up', 'mount', 'climb']}, 
				u'一': {'article': ['a', 'one'], 'adjective':['single']}, 
				u'株': {'noun': ['share', 'stock', 'stump']}, 
				u'玫瑰花': ['rose'],  
				u'不久前': ['not long ago'], 
				u'它': {'pronoun':['it']},  
				u'還十分': ['also very'],  
				u'嬌艶': ['jiao yan-'], 
				u'、': {'punctuation': [',']},  
				u'充滿': {'adjective':['full', 'brimming', 'very full'], 'noun':['fullness', 'fulness', 'perfusion'], 'verb':['fall upon']},
				u'青春': {'noun':['youth', 'prime', 'bloom', 'adolescence', 'adolescency', 'May']},  
				u'活力': {'noun': ['vitality', 'vigor', 'energy', 'vigour']},
				u'而':{'conjunction': ['and', 'while', 'but', 'yet', 'as well as']}, 
				u'我的選擇': ['my choice'], 
				u'就算犯': ['even if guilty'], 
				u'錯挨罵': ['wrong scolded'], 
				u'也': {'adverb': ['also', 'too']},  
				u'要': {'verb': ['want', 'desire', 'must', 'wish', 'ask', 'demand', 'request', 'coerce', 'force', 'ask to do'], 'adjective':['important', 'vital'], 'conjunction':['if']}, 
				u'昂首': ['head'],  
				u'闊': {'adjective': ['wide', 'broad', 'rich', 'vast', 'wealthy'], 'noun':['broad', 'broadness']},  
				u'步': {'noun': ['step', 'pace', 'stage', 'footsteps'], 'adjective':['walking'], 'verb':['walk', 'foot', 'tread', 'go on foot', 'stage in a process']},
				u'他':{'pronoun': ['he', 'him'], 'adjective':['allochromatic'], 'noun':['hillside']}, 
				u'用': {'noun': ['use', 'usefulness', 'need','expense', 'outlay'], 'verb':['use', 'apply', 'take','eat']}, 
				u'僅會': ['only'], 
				u'中文': {'noun':['chinese']},  
				u'單字': {'noun': ['individual character', 'separate character']},  
				u'或是': ['or'], 
				u'比': {'noun': ['ratio'], 'verb':['compare', 'contrast', 'compete', 'emulate'], 'particle':['particle used for comparison']},  
				u'手畫腳': ['hands and feet'],  
				u'爸媽': ['mom and dad'],  
				u'溝通': {'noun':['communication'], 'verb':['communicate']},
				u'安葬': {'verb':['tomb', 'bury the dead']}, 
				u'日子': {'noun': ['day', 'date', 'life', 'when','days of life']}, 
				u'到': {'verb':['go to', 'reach', 'get to', 'arrive', 'leave for', 'compass'], 'adverb':['up', 'up until']}, 
				u'來了': ['coming'],
				u'不出': ['no'], 
				u'年': {'noun': ['year', 'New Year', 'age', 'harvest']}, 
				u'皇后': {'noun': ['empress']}, 
				u'果然': {'adverb':['really', 'sure enough', 'certainly', 'as expected']}, 
				u'生': {'adjective':['raw', 'living','green','unripe','crude','uncooked'], 'noun':['life','student','livelihood'], 'verb':['give birth', 'grow', 'be born']},  
				u'位': {'noun':['position', 'place', 'digit', 'figure', 'location', 'seat', 'throne']},  
				u'公主': {'noun': ['princess']},
				u'很': {'adverb':['very', 'quite','extremely', 'passing', 'strongly','strong','mighty','bitterly','spanking','parlous']},  
				u'久': {'adverb':['long'], 'noun':['long time']}, 
				u'很久以前': ['a long time ago'], 
				u'個': {'adjective':['individual'], 'noun':['piece', 'general classifier'], 'pronoun':['oneself'], 'auxiliary verb':['universal measure word']},  
				u'可愛': {'adjective':['cute', 'lovely', 'amiable']},  
				u'小': {'adjective':['small', 'little', 'tiny','young','few','tabloid','bitty']},  
				u'女孩': {'noun':['girl','lass']}, 
				u'跟': {'preposition':['with'], 'noun':['follow', 'heel'], 'verb':['follow', 'go with'], 'conjunction':['and']},  
				u'爸爸': {'noun':['father', 'pappy']}, 
				u'媽媽': {'noun':['mom', 'mama', 'momma','mamma']},  
				u'住在': ['living in'],  
				u'小村': ['little village'], 
				u'莊裏': ['woman in this town'],
				u'燕子': ['swallow'], 
				u'在': {'preposition':['in', 'at'], 'verb':['be', 'exist', 'remain', 'dwell', 'be alive', 'belong to an organization', 'be located somewhere', 'depends']}, 
				u'崎嶇': {'adjective':['rugged']}, 
				u'崖道': ['cliff road'], 
				u'旁': {'preposition':['beside'], 'noun':['side'], 'adverb':['else'], 'adjective':['irresolute', 'other']}, 
				u'築巢': {'verb':['nest']},  
				u'土坡': ['slopes'],  
				u'上啄': ['the pecking'], 
				u'出': {'verb':['come out', 'issue', 'go out', 'turn out', 'arise', 'put forth', 'put up','vent','exceed','happen','expend']},  
				u'洞': {'noun': ['hole', 'cave', 'tear'], 'adverb':['thoroughly']},
				u'鼓起': {'verb':['muster', 'summon', 'pluck up', 'summon up', 'plump', 'marshal', 'heave', 'knob', 'call up'], 'adjective':['plump', 'buxom'], 'noun':['heave']}, 
				u'勇氣': {'noun':['courage', 'valor', 'valour', 'nerve', 'audacity']}, 
				u'去': {'noun':['go'], 'verb':['go', 'remove', 'leave']}, 
				u'否則': {'adverb':['otherwise', 'else'], 'conjunction':['if not']},  
				u'明天': {'adverb':['tomorrow'], 'noun':['tomorrow', 'morrow', 'morn']}, 
				u'一早': ['morning'],  
				u'將變': ['will become'],  
				u'成': {'verb':['become', 'complete', 'finish', 'turn into', 'succeed','win', 'accomplish'], 'adjective':['capable']}, 
				u'泡泡': ['bubble'],  
				u'死去': ['dead'], 
				u'們必須': ['we must'], 
				u'按照': {'preposition': ['according to', 'on the basis of', 'in the light of']}, 
				u'正確': {'adjective': ['correct', 'proper']}, 
			 	u'的': {'preposition': ['of'], 'noun': ['aim'], 'adverb': ['really and truly'], 'particle': ['possessive particle'], 'auxiliary verb': ['ablative cause suffix'], 'suffix': ['-self']}, 
			 	u'原則辦事': ['principles act'], 
			 	u'！':{'punctuation': ['!']},
				u'次': {'adjective':['secondary'], 'noun':['order', 'number','bout','sequence']}, 
				u'坐': {'verb':['sit', 'take a seat', 'put', 'travel by']}, 
				u'捷運邊': ['MRT edge'], 
				u'邊玩': ['while playing'],  
				u'還': {'adverb':['also', 'still','yet','not yet','in addition','else','more'], 'verb':['return', 'pay back'], 'adjective':['any more']}, 
				u'忘我': ['ecstasy'],  
				u'到': {'verb':['go to', 'reach', 'get to', 'arrive', 'leave for', 'compass'], 'adverb':['up','up until']}, 
				u'坐過頭': ['sat head'],  
				u'多站': ['multistation'], 
				u'；':{'punctuation': [';']}}

poss_pronoun_dict = { 	'I':'my', 
						'me':'my', 
						'you':'your', 
						'he':'his', 
						'him':'his', 
						'she':'her', 
						'it':'its', 
						'we':'our', 
						'us':'our', 
						'they':'their', 
						'them':'their'}

###Program Execution Calls##

#Bilingual Dictiony Already Built in BilingualDict.py - imported here for use
#Building English Unigram Dictionary
english_unigrams = trainUnigrams()

#devset filname: 'tokenized_devset'
#testset filename: 'tokenized_testset'

print '\n -------Baseline Translation------'
generateTranslation(bilingual_dict, english_unigrams, '../corpus/tokenized_testset', True)

print '\n -------Strategy #1: Unigram Frequency Model------'
generateTranslation(bilingual_dict, english_unigrams, '../corpus/tokenized_testset', False)

print '\n -------Strategy #2 POS Tagging and Back-off to Unigram Frequency Model------'
generateWithPOS(bilingual_dict, english_unigrams, '../corpus/tokenized_testset')

print '\n -------Strategies #3-6 FINAL TRANSLATION------'
generateFinalTranslations(bilingual_dict, english_unigrams, '../corpus/tokenized_testset')