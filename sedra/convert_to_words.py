import csv

# Consonants: A B G D H O Z K Y ; C L M N S E I / X R W T
# Vowels:     a o e i u
# Diacretics: '  dot above, Qushaya
#	 ,  dot below, Rukkakha
#	 _  line under
#	 *  Seyame

SYRIAC = {
'A' : u'\u0710',
'B' : u'\u0712',
'G' : u'\u0713',
'D' : u'\u0715',
'H' : u'\u0717',
'O' : u'\u0718',
'Z' : u'\u0719',
'K' : u'\u071A',
'Y' : u'\u071B',
';' : u'\u071D',
'C' : u'\u071F',
'L' : u'\u0720',
'M' : u'\u0721',
'N' : u'\u0722',
'S' : u'\u0723',
'E' : u'\u0725',
'I' : u'\u0726',
'/' : u'\u0728',
'X' : u'\u0729',
'R' : u'\u072A',
'W' : u'\u072B',
'T' : u'\u072C',
'a' : u'\u0730',
'o' : u'\u0733',
'e' : u'\u0736',
'i' : u'\u073A',
'u' : u'\u073D',
"'" : u'\u0741', # '  dot above, Qushaya
',' : u'\u0742',#	 ,  dot below, Rukkakha
'_' : u'\u0748',#	 _  line under
'*' : u'\u0705',# *  Seyame
'-': '-'
}

def convert_to_unicode(w):
	return ''.join([SYRIAC[x] for x in w.replace('**', '')])


def to_16_bits(n):
	return '{0:16b}'.format(n)


def convert_to_line_number(x):
	return int(hex(int(x, 10)).replace('0x', '')[1:], 16)

def read_lemmas():
	with open('tblLexemes.txt', 'r') as f:
		reader = csv.reader(f)
		out = {}
		first_skipped = False
		for line in reader:
			if first_skipped:
				lnum = line[0]
				lemma = line[2]
				out[lnum] = lemma
			else:
				first_skipped = True
		return out


def read_english():
	with open('tblEnglish.txt', 'r') as f:
		reader = csv.reader(f)
		out = {}
		first_skipped = False
		for line in reader:
			if first_skipped:
				# _, lnum, gloss, gl1, gl2, _ = line.split(',', maxsplit=5)
				lnum = line[1]
				gloss = line[2]
				gl1 = line[3]
				gl2 = line[4]
				out[lnum] = f"{gl1} {gloss} {gl2}".strip()
			else:
				first_skipped = True
		return out



SUFFIX_GENDER = {'0': 'C', '1': "M", '2': "F"}
GENDER = {'0': '', '1': 'C', '2': "M", '3': "F"}
PERSON = {'0' :'', '1': '3', '2': '2', '3': '1'}
SUFFIX_NUMBER = {'0' :'S', '1': 'P'}
NUMBER = {'0' :'', '1': 'S', '2': 'P'}
STATE = {'0': '', '1' :'ABS', '2': 'CON', '3': 'EMP'}
TENSE = {'0' : '', '1': "P", '2': 'I', '3': 'M', '4': 'N', '5':'PA', '6' : 'PP', '7' : 'Ps'}
FORM = {'0': '',
'1' : 'PEAL',
'2' : 'ETHPEAL',
'3' : 'PAEL',
'4' : 'ETHPAEL',
'5' : 'APHEL',
'6' : 'ETTAPHAL',
'7' : 'SHAPHEL',
'8' : 'ESHTAPHAL',
'9' : 'SAPHEL',
'10' : 'ESTAPHAL',
'11' : 'PAUEL',
'12' : 'ETHPAUAL',
'13' : 'PAIEL',
'14' : 'ETHPAIAL',
'15' : 'PALPAL',
'16' : 'ETHPALPAL',
'17' : 'PALPEL',
'18' : 'ETHPALPAL',
'19' : 'PAMEL',
'20' : 'ETHPAMAL',
'21' : 'PAREL',
'22' : 'ETHPARAL',
'23' : 'PALI',
'24' : 'ETHPALI',
'25' : 'PAHLI',
'26' : 'ETHPAHLI',
'27' : 'TAPHEL',
'28' : 'ETHAPHAL'}


#"keySeyame","keyListingType","keyEnclitic",
#"keyIsLexeme","keySuffixGender","keySuffixPerson",
#"keySuffixNumber","keySuffixContraction","keyPrefix",
#"keyGender","keyPerson","keyNumber","keyState",
#"keyTense","keyForm"

def format_parse(xs):
	semaye = xs[0]
	#listing_type = xs[1]
	is_enclitic = xs[2]
	#keyIsLexeme = xs[3]
	suffix_gender = SUFFIX_GENDER[xs[4]]
	suffix_person = PERSON[xs[5]]
	suffix_num = SUFFIX_NUMBER[xs[6]]
	suffix = '' if suffix_person == '' else f"|{suffix_person}{suffix_gender}{suffix_num}"
	gender = GENDER[xs[9]]
	person = PERSON[xs[10]]
	num = NUMBER[xs[11]]
	state = STATE[xs[12]]
	tense= TENSE[xs[13]]
	form = FORM[xs[14]]
	return f"{form} {gender}{person}{num} {state} {tense} {suffix}".replace('  ', ' ').strip().replace(' ','-')


def read_words(glosses, lemmas):
	with open('tblWords.txt', 'r') as f:
		reader = csv.reader(f)
		out = {}
		first_skipped = False
		for line in reader:
			if first_skipped:
				#lnum, lemma, w, pointed, data = line.split(',', maxsplit=4)
				lnum = line[0]
				lemma = line[1]
				w = convert_to_unicode(line[2])
				pointed = convert_to_unicode(line[3])
				data = format_parse(line[4:])
				gl = glosses[lemma] if lemma in glosses else '!!!'
				lem = convert_to_unicode(lemmas[lemma]) if lemma in lemmas else '!!!'
				out[int(lnum)] = (w, pointed, data, lem, gl)
			else:
				first_skipped = True
		return out




glosses = read_english()
lemmas = read_lemmas()
words = read_words(glosses, lemmas)


with open('BFBS.TXT', 'r') as f:
	for line in f:
		_, ref, word, _ = line.strip().split(',')
		line_number = convert_to_line_number(word)
		if line_number in words:
			w, pointed, data, lemma, gloss = words[line_number]
			print(f"{ref}\t{w}\t{pointed}\t{lemma}\t{gloss}\t{data}")
		else:
			print(f"{ref}\t!!{word}!!")
			break
