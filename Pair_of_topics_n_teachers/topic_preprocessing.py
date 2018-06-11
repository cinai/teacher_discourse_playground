# -*- coding: utf-8 -*-
import re
import numpy as np
import nltk
#import spellChecker as sc
from collections import Counter

'''
Words to be masked
'''
set_conectores_aditivos = ["más aún", "todavía más", "incluso", "así mismo", "de igual modo","igualmente", "por otro lado", "también", "tampoco", "además"]
set_conectores_adversativos = ["no obstante", "por el contrario", "aun asi", "aun así","ahora bien", "de todas formas", "despues de todo", "en contraste", "por otra parte", "en cambio", "tampoco", "pero", "más que","sin embargo"]
set_conectores_consecutivos = [ "porque","ya que", "debido", "dado que", "pues", "pues bien", "puesto que","entonces", "asi pues", "por ello", "a casusa", "por ende", "en consecuencia", "por consiguiente","de modo que", "por lo tanto"]
set_conectores_condicionales = ["en vista","por supuesto", "aun que","aunque","aun cuando", "a pesar"]
set_conectores_explicativos = ["es decir","osea", "o sea","en otras palabras","en otra palabras"]
set_conectores_conclusion = ["en resumen", "en suma", "dicho de otro modo", "en síntesis", "finalmente", "concluyendo", "en conclusión", "por último", "sintetizando"]
set_conectores_ejemplificacion = ["por ejemplo", "ejemplo","asi", "así como","asi como", "para ilustrar", "es decir", "osea", "o sea"]
set_conectores_temporales_posterioridad = ["más tarde", "luego", "después", "posteriormente"]
set_conectores_espaciales = ["al lado", "alado", "abajo","izquierda", "derecha", "medio", "fondo", "junto a","junto", "debajo", "aquí", "allá","allí", "acá"]

set_comparacion = ["es como", "es similar",  "análogo","es semejante", "es parecido"]
set_emocional_positiva = ["bien", "vien", "buena", "bueno", "bonito", "bonita", "bn", "increible", "excelente","exelente","eselente","erselente","eccelente",  "favuloso", "fabuloso", "emocionante","emosionante", "imprecionante","impresionante","inprecionante","inpresionante","marabilloso","maravilloso","marabiyoso","maraviyoso", "espectacular","bacan", "bakan", "bkn"]#, ":)", ":D", ";)", "<3", 
set_emocional_negativa = ["mala","malo","mal", "maldad", "lata", "fome", "feo","fea", "horrible", "malvada", "malvado","desagradable", "incomodo", "nefasto", "funesto", "tragedia","tragico", "desdicha", "desgracia", "miedo", "tenebroso", "pauperrimo"]#,":c", ":(", ":C"

preg_pal_porque = ["por qué","por que"]#,"por que","porque","pq"]
preg_pal_explica = ["expliq","explica","explic","expliquen","explique"]

# read stop words
#STOPWORDS = re.findall(r'\w+',open('../data/stop_spanish.txt').read())

# STEMMER
#STEMMER = nltk.SnowballStemmer('spanish')

def stemming(word):
    if word == word.lower():
        return STEMMER.stem(word)
    else:
        return word
  
def replace_words(x):
    for y in set_conectores_aditivos:
        x = x.replace(y,'CONECTOR_ADITIVO')
    for y in set_conectores_adversativos:
        x = x.replace(y,'CONECTOR_ADVERSATIVO')
    for y in set_conectores_consecutivos:
        x = x.replace(y,'CONECTOR_CONSECUTIVO')
    for y in set_conectores_condicionales:
        x = x.replace(y,'CONECTOR_CONDICIONAL')
    for y in set_conectores_explicativos:
        x = x.replace(y,'CONECTOR_EXPLICATIVO')
    for y in set_conectores_ejemplificacion:
        x = x.replace(y,'CONECTOR_EJEMPLO')
    for y in set_conectores_temporales_posterioridad:
        x = x.replace(y,'CONECTOR_TEMPORAL_POST')
    for y in set_conectores_espaciales:
        x = x.replace(y,'CONECTOR_ESPACIAL')
    for y in set_comparacion:
        x = x.replace(y,'CONECTOR_COMPARACION')
    for y in set_emocional_positiva:
        x = x.replace(y,'EMOCION_POSIT')
    for y in set_emocional_negativa:
        x = x.replace(y,'EMOCION_NEG')
    for y in preg_pal_porque:
        x = x.replace(y,'POR_QUE')
    for y in preg_pal_explica:
        x = x.replace(y,'EXPLICA')
    return x
# Preprocessing Function
def preprocessing(x, isexample = False, withStopWords = False, withStemming = True, withSpellChecker = True):
    # x: string. A sentence.
    # output: list of stemmed words in order.
    
    if isexample:
        print('Original text:')
        print('\t'+x)
    
    # lowercase
    x = x.lower()
    if isexample:
        print('lowercase:')
        print('\t'+x)

    x = replace_words(x)
    #remove symbols
    x = re.sub("[^\w]", " ", x)
    if isexample:
        print('Remove Symbols:')
        print('\t'+x)
    
    #transform numbers to DIGIT
    x = re.sub("[\d]","DIGIT",x)
    if isexample:
        print('Numbers to DIGIT:')
        print('\t'+x)
    
    return wordList

def preprocessList(X):
    wordSentenceList = [preprocessing(x, withSpellChecker = False, withStemming = False) for x in X]
    wordList = [x for S in wordSentenceList for x in S]
    dictFreq = Counter(wordList)
    dictionary = list(dictFreq.keys())
    dictCorrected = dictionary
    dictCorrected = [sc.correction(x) for x in dictCorrected]
    dictCorrected = [stemming(x) for x in dictCorrected]
    dictMatch = dict(zip(dictionary,dictCorrected))
        
    dictRepresent = dict()
    for t in list(set(dictCorrected)):
        candidates = [x for x in dictionary if dictMatch[x]==t]
        maxFreq = max([dictFreq[x] for x in candidates])
        candidates = [x for x in candidates if dictFreq[x]==maxFreq]
        dictRepresent[t] = candidates[0]
    dictRepresent['WHY'] = 'por qué'
    
    res = [ [dictRepresent[dictMatch[x]] for x in S] for S in wordSentenceList]                  
                      
        
    return res


def createDictionary(wordSentenceList):
    wordSets = [list(set(x)) for x in wordSentenceList]
    dictionary = sorted(list(set([x for s in wordSets for x in s])))
    return dictionary


def tdmtx(wordSentenceList,dictionary):
    return np.array([ np.array([d in s for d in dictionary])*1 for s in wordSentenceList])


def tf_idf_mtx(wordSentenceList):
    dictionary = createDictionary(wordSentenceList)
    tfmtx = np.array([np.array([x.count(d) for d in dictionary]) for x in wordSentenceList])
    N = len(wordSentenceList)
    idfmtx = np.matlib.repmat(np.log(N/np.sum(tfmtx>0,axis=0)),N,1)
    tf_idf = tfmtx*idfmtx
    return tf_idf
    
    

def minfo_pairs(wordSentenceList,dictionary,th = 10):
	mtx = tdmtx(wordSentenceList,dictionary)
	comtx = np.matmul(np.transpose(mtx),mtx)
	p1word = np.diag(comtx)/(mtx.shape[0])
	triup = np.triu(comtx*(comtx>th),1)
	wa, wb = np.nonzero(triup)
	rawcount = triup[wa,wb]
	p2words = rawcount/mtx.shape[0]
	minfo = np.log2(p2words/(p1word[wa]*p1word[wb]))
	sort_idx = np.argsort(-minfo)
	sort_minfo = minfo[sort_idx]
	tempa = [dictionary[x] for x in wa[sort_idx]]
	tempb = [dictionary[x] for x in wb[sort_idx]]
	return [tempa, tempb, sort_minfo]