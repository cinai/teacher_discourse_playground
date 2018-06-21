# -*- coding: utf-8 -*-
'''
Module that prepare a list of documents to be processed with LDA.
'''

import re
import numpy as np
import nltk
#import spellChecker as sc
from collections import Counter
from nltk.corpus import stopwords

'''
Words to be masked
'''
set_conectores_aditivos = ["más aún", "todavía más", "incluso", "así mismo",
                           "de igual modo","igualmente", "por otro lado", 
                           "también", "tampoco", "además"]

set_conectores_adversativos = ["no obstante", "por el contrario", "aun asi", 
                               "aun así","ahora bien", "de todas formas", 
                               "despues de todo", "en contraste", 
                               "por otra parte", "en cambio", "tampoco", "pero", 
                               "más que","sin embargo"]

set_conectores_consecutivos = ["porque","ya que", "debido", "dado que", 
                               "pues bien","pues","puesto que","entonces",
                               "asi pues","por ello", "a causa", "por ende",
                               "en consecuencia", "por consiguiente",
                               "de modo que","por lo tanto"]

set_conectores_condicionales = ["en vista","por supuesto", "aun que","aunque",
                                "aun cuando", "a pesar"]

set_conectores_explicativos = ["es decir","osea", "o sea","en otras palabras",
                               "en otra palabras"]

set_conectores_conclusion = ["en resumen", "en suma", "dicho de otro modo", 
                             "en síntesis", "finalmente", "concluyendo", 
                             "en conclusión", "por último", "sintetizando"]

set_conectores_ejemplificacion = ["por ejemplo", "ejemplo","asi", "así como",
                                  "asi como", "para ilustrar", "es decir"]

set_conectores_temporales_posterioridad = ["más tarde", "luego", "después", 
                                           "posteriormente"]

set_conectores_espaciales = ["al lado", "alado", "abajo","izquierda", 
                             "derecha", "medio", "fondo", "junto a","junto", 
                             "debajo", "aquí", "allá","allí", "acá"]

set_comparacion = ["es como", "es similar",  "análogo","es semejante",
                   "es parecido"]

set_emocional_positiva = ["bien", "buena", "bueno", "bonito", "bonita", 
                          "increíble", "excelente","fabuloso", "emocionante",
                          "impresionante","maravilloso","espectacular",
                          "bacan", "bakan", "bkn","perfecto"]

set_emocional_negativa = ["mala","malo","mal", "maldad", "lata", "fome",
                          "feo","fea", "horrible", "malvada", "malvado",
                          "desagradable", "incómodo", "nefasto", "funesto",
                          "tragedia","trágico", "desdicha", "desgracia", 
                          "miedo", "tenebroso", "paupérrimo"]

preg_pal_porque = ["por qué","por que"]#,"por que","porque","pq"]

preg_pal_explica = ["explica","expliquen","explique"]

set_direccion = ['tienes que','tienen que','vamos a','van a','hay que','hagan','hagamos','haga','tiene que','tenemos que']

set_administracion = ['señorita','señor','por favor','advertencia','puedo avanzar','usted']

set_to_be_replaced = {}

set_to_be_replaced['TAMBIEN_TAMPOCO'] = set_conectores_aditivos
set_to_be_replaced['EN_CAMBIO'] = set_conectores_adversativos
set_to_be_replaced['YA_QUE'] = set_conectores_consecutivos
set_to_be_replaced['AUNQUE'] = set_conectores_condicionales

set_to_be_replaced['ES_DECIR'] = set_conectores_explicativos
set_to_be_replaced['POR_ULTIMO'] = set_conectores_conclusion
set_to_be_replaced['POR_EJEMPLO'] = set_conectores_ejemplificacion
set_to_be_replaced['LUEGO'] = set_conectores_temporales_posterioridad

set_to_be_replaced['AQUI_ALLA'] = set_conectores_espaciales
set_to_be_replaced['ES_COMO'] = set_comparacion
set_to_be_replaced['BIEN'] = set_emocional_positiva
set_to_be_replaced['MAL'] = set_emocional_negativa

set_to_be_replaced['POR_QUE'] = preg_pal_porque
set_to_be_replaced['EXPLICA'] = preg_pal_explica
set_to_be_replaced['TIENES_QUE'] = set_direccion
set_to_be_replaced['ADMINISTRACION'] = set_administracion
set_to_be_replaced['A_NAME'] = ['a_name']

# read stop words
STOPWORDS = stopwords.words('spanish') + ['está','va','si']

# replace words in a string according to the sets defined above
def replace_words(x):
    for key,value in set_to_be_replaced.items():
        text = ' '+key+' '
        for y in value:
            my_regex = r'\s?'+re.escape(y)+r'[\s.,;\-!:]?'
            x = re.sub(my_regex,text,x)
    return x

# STEMMER
STEMMER = nltk.SnowballStemmer('spanish')

def stemming(word):
    word = word.decode('utf-8')
    if word == word.lower():
        return word[:7]
    else:
        return word

with open('names.txt','rb') as f:
    NAMES = [x.rstrip() for x in reversed(f.readlines())]

def detect_names(x):
    text = ' A_NAME '
    for y in NAMES:
        my_regex = r'\s'+re.escape(y)+r'[\s.,;\-!:]?'
        x = re.sub(my_regex,text,x)
    return x

# Preprocessing Function
def preprocessing(x,isexample=False,withStopWords=False,withStemming=False):
    # x: string. A sentence.
    # output: list of stemmed words in order.
    
    if isexample:
        print('Original text:')
        print('\t'+x)

    # replace all names with a tag 
    x = detect_names(x)
    if isexample:
        print('Nombres:')
        print('\t'+x)

    # lowercase
    x = x.lower()
    if isexample:
        print('lowercase:')
        print('\t'+x)

    x = replace_words(x)

    #transform numbers to NUMBER
    x = re.sub('[-+]?\d*,?\d+',' NUMBER ',x)
    if isexample:
        print('Numbers to NUMBER:')
        print('\t'+x)

    #remove symbols
    #my_regex = r'[^\w]'
    #x = re.sub(my_regex, ' ', x)

    x = x.replace(',',' ')
    x = x.replace('*',' ')
    x = x.replace(':',' ')
    x = x.replace(';',' ')
    x = x.replace('.',' ')
    x = x.replace('-',' ')
    
    if isexample:
        print('Remove Symbols:')
        print('\t'+x)

    #remove stop words
    wordList = x.split()
    if not(withStopWords):
        wordList = [x for x in wordList if x not in STOPWORDS]
        if isexample:
            print("Remove Stop Words:")
            print(wordList)

    #stemming
    if withStemming:
        wordList = [stemming(x) for x in wordList]
        if isexample:
            print("Stemming:")
            print(wordList)

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



'''
for y in set_conectores_adversativos:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_ADVERSATIVO',
        x = re.sub(my_regex,text,x)
    for y in set_conectores_consecutivos:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_CONSECUTIVO'
        x = re.sub(my_regex,text,x)
    for y in set_conectores_condicionales:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_CONDICIONAL'
        x = re.sub(my_regex,text,x)
    for y in set_conectores_explicativos:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_EXPLICATIVO'
        x = re.sub(my_regex,text,x)
    for y in set_conectores_ejemplificacion:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_EJEMPLO'
        x = re.sub(my_regex,text,x)
    for y in set_conectores_temporales_posterioridad:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_TEMPORAL_POST'
        x = re.sub(my_regex,text,x)
    for y in set_conectores_espaciales:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_ESPACIAL'
        x = re.sub(my_regex,text,x)
    for y in set_comparacion:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'CONECTOR_COMPARACION'
        x = re.sub(my_regex,text,x)
    for y in set_emocional_positiva:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'EMOCION_POSIT'
        x = re.sub(my_regex,text,x)
    for y in set_emocional_negativa:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'EMOCION_NEG'
        x = re.sub(my_regex,text,x)
    for y in preg_pal_porque:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'POR_QUE'
        x = re.sub(my_regex,text,x)
    for y in preg_pal_explica:
        my_regex = r"\b" + re.escape(y) + r"\b"
        text = 'EXPLICA'
        x = re.sub(my_regex,text,x)
'''