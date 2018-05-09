# -*- coding: utf-8 -*-
# text_preprocessing module

import nltk
import os
import re
from nltk.corpus import stopwords
from pydub import AudioSegment

tokenize = lambda doc: nltk.word_tokenize(doc.lower())

'''
Sets of words
'''
set_conectores_aditivos = ["más aún", "todavía más", "incluso", "así mismo", "de igual modo","igualmente", "por otro lado", "también", "tampoco", "además"]
set_conectores_adversativos = ["no obstante", "por el contrario", "aún así", "ahora bien", "de todas formas", "después de todo", "en contraste", "por otra parte", "en cambio", "tampoco", "pero", "más que"]
set_conectores_consecutivos = [ "porque","ya que", "debido", "dado que", "pues", "pues bien", "puesto que","entonces", "así pues", "por ello", "a casusa", "por ende", "en consecuencia", "por consiguiente","de modo que", "por lo tanto"]
set_conectores_condicionales = ["en vista", "por supuesto", "aunque","aún cuando", "a pesar"]
set_conectores_explicativos = ["es decir","osea","en otras palabras"]
set_conectores_conclusion = ["en resumen", "en suma", "dicho de otro modo", "en síntesis", "finalmente", "concluyendo","en conclusión","por último", "sintetizando"]
set_conectores_ejemplificacion = ["por ejemplo","ejemplo","asi", "asi como", "para ilustrar", "es decir", "osea"]
set_conectores_temporales_posterioridad = ["más tarde", "luego", "después", "posteriormente"]
set_conectores_espaciales = ["al lado", "abajo","izquierda", "derecha", "medio", "fondo", "junto a","junto", "debajo","aquí", "allá","allí"]
set_conectores_temporales_anterioridad = ["antes", "hace tiempo", "habia una vez", "al principio","al comienzo", "previamente", "en primer lugar", "inicialmente"]
set_conectores_temporales_simultaneidad = ["en este instante", "al mismo tiempo", "mientras", "mientras tanto", "mientras que", "a la vez", "entonces",  "simultaneamente", "actualmente","a medida"]
set_conectores = set_conectores_aditivos+set_conectores_adversativos+set_conectores_consecutivos+set_conectores_condicionales+ \
                 set_conectores_explicativos+set_conectores_conclusion+set_conectores_ejemplificacion+ \
                 set_conectores_temporales_posterioridad+set_conectores_espaciales+set_conectores_temporales_anterioridad+set_conectores_temporales_simultaneidad

set_emocional_positiva = ["bien", "buena", "bueno", "bonito", "bonita", "increíble", "excelente","fabuloso", "emocionante","impresionante","maravilloso","espectacular","bacan", "bacán"]#, ":)", ":D", ";)", "<3", 
set_emocional_negativa = ["mala","malo","mal", "maldad", "lata", "fome", "feo","fea", "horrible", "malvada", "malvado","desagradable", "incómodo", "nefasto", "funesto", "tragedia","trágico", "desdicha", "desgracia", "miedo", "tenebroso", "paupérrimo"]#,":c", ":(", ":C"
set_opinion = ["creo","pienso","me parece"]
set_expresion = set_opinion+set_emocional_negativa+set_emocional_positiva
set_comparacion = ["es como", "es cimilar","es similar","análogo","es semejante", "es parecido"]
set_palabra_modelo = ["modelo"]

preg_pal_porque = ["por qué"]#,"por que","porque","pq"]
preg_pal_explica = ["explique","expliquen","explica"]
preg_pal_como = ["cómo"]
preg_explicacion = preg_pal_porque+preg_pal_explica+preg_pal_como
preg_pal_cual = ["cuál"]
preg_pal_cuando = ["cuándo"]
preg_pal_cuanto = ["cuánto"]

set_preguntas = preg_explicacion+preg_pal_cuanto+preg_pal_cuando

set_experimentos = ["experiment", "evidencia", "hipótesis", "muestra", "medi","investiga", "efecto", "causa", "diseño", "explic", "cambio", "variable", 
                     "relaci", "resultado", "conclusio", "gráfico","model"]
set_electricidad = ["eléctrico","eléctrica","eléctricos","eléctricas","electricidad","circuito","circuitos","mixtos","corriente","corrientes",
"conducto","conductor","conductores",
"ampolleta","material","materiales","resistente","resistencia","resistencias","resistentes",
"aislante","aislantes"
"cargas","carga"
"voltaje","voltajes","cables","cable","interruptor","interruptores","intensidad","intensidades"]

set_all = set_electricidad + set_experimentos + set_preguntas + set_comparacion + set_expresion + set_conectores


#--- Read Documents---

# Notese: Hay que seleccionar una funcion read_documents apropiada
# a la estructura del path donde se encuentran los archivos.

# read_documents: string -> {string: [string]}
# lee los documentos contenidos en una carpeta
# y retorna un diccionario de los documentos 
# encontrados.
# Asumen que los documentos estan en una carpeta
# donde cada carpeta tiene un archivo txt del mismo nombre.
def read_documents(path_documents):
    dict_documents = {}
    for folder in os.listdir(path_documents):
        folder_a = os.path.join(path_documents,folder)
        f = open(os.path.join(folder_a,folder+'.txt'),'rb')
        aux_doc = f.read()
        f.close()
        dict_documents[folder] = aux_doc
    return dict_documents

# read_documents_2: string -> [string],[[string]]
# lee los documentos contenidos en una carpeta
# y retorna una lista de los nombres de documentos 
# encontrados, y una lista de listas de strings.
# Asumen que los documentos estan agrupados en subcarpetas
# por grado y tema.
def read_documents_2(path_documents):
    all_documents = []
    name_documents = []
    for folder in os.listdir(path_documents):
        folder_a = os.path.join(path_documents,folder)
        for folder_b in os.listdir(folder_a):
            for folder_c in os.listdir(os.path.join(folder_a,folder_b)):
                name_documents.append(folder+'_'+folder_b+'_'+folder_c)
                f = open(os.path.join(os.path.join(folder_a,folder_b),folder_c,folder_c+'.txt'),'rb')
                aux_doc = f.read()
                f.close()
                all_documents.append(aux_doc)
    return name_documents,all_documents

import unidecode
import sys
# List tree structure of a path
def list_files(startpath):
    for folder_grade in os.listdir(startpath):
        level = folder_grade.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(folder_grade)))
        subindent = ' ' * 4 * (level + 1)
        for folder_subject in os.listdir(os.path.join(startpath,folder_grade)):
            subject_path = os.path.join(startpath,folder_grade,folder_subject)
            s = folder_subject.decode(sys.getfilesystemencoding())
            print('{}{}'.format(subindent, '')+s+'('+str(len([f for f in os.listdir(subject_path)]))+')')


# List tree structure of a path
def get_dict_files_with_grade_and_content(startpath):
    dict_files = {}
    for folder_grade in os.listdir(startpath):
        level = folder_grade.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        subindent = ' ' * 4 * (level + 1)
        for folder_subject in os.listdir(os.path.join(startpath,folder_grade)):
            subject_path = os.path.join(startpath,folder_grade,folder_subject)
            s = folder_subject.decode(sys.getfilesystemencoding())
            for f in os.listdir(subject_path):
                dict_files[f] = {'grade': folder_grade,'content': s}
    return dict_files

def get_labels_by_document(names,dict_with_labels):
    new_labels = []
    for i in range(len(names)):
        aux_dict = dict_with_labels[names[i]]
        a_name = aux_dict['content'].replace(' ','_')
        final_name = aux_dict['grade'].upper()+'_'+a_name
        new_labels.append(final_name.encode('utf8') )
    return new_labels

#--- Describe Documents---
def get_length_document_in_minutes(all_documents,audio_path):
    dict_length = {}
    audio_files = os.listdir(audio_path)
    for d in all_documents:
        file_name = d+'.wav'
        if file_name in audio_files:
            audio_file = AudioSegment.from_wav(os.path.join(audio_path,file_name))
            duration_min = round((len(audio_file)/(1000.0*60)),2)
            dict_length[d] = duration_min
    return dict_length

def get_all_token_set(dict_documents):
    tokenized_documents = []
    for key in dict_documents.keys():
        tokenized_documents.append(tokenize(dict_documents[key]))
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    return all_tokens_set

def get_frequency_per_word(dict_documents,all_tokens_set=[]):
    if all_tokens_set == []:
        all_tokens_set = get_all_token_set(dict_documents)
    all_documents = ""
    for key in dict_documents.keys():
        all_documents += dict_documents[key].lower()
    tokenized_documents = tokenize(all_documents)
    term_freq = []
    for term in all_tokens_set:
        term_count = 0
        term_freq.append(tokenized_documents.count(term))
    return term_freq

#--- Filter Documents---
def get_filter_by_frequency(token_set,frequency_per_word,min_freq,filter_stop_words=True):
    zipped = zip(token_set,frequency_per_word)
    zipped.sort(key = lambda t: t[1], reverse=True)
    selected_words = []
    for  i in range(len(zipped)):
        if zipped[i][1] >= min_freq:
            selected_words.append(zipped[i][0])
    return selected_words

def get_filter_by_number(token_set,frequency_per_word,total_number,filter_stop_words=True):
    stop_words_spanish = stopwords.words('spanish')
    zipped = zip(token_set,frequency_per_word)
    zipped.sort(key = lambda t: t[1], reverse=True)
    selected_words = []
    counter = 0
    for  i in range(len(zipped)):
        if counter < total_number:
            a_word = zipped[i][0]
            if (filter_stop_words and a_word in stop_words_spanish) or (a_word != '?' and not a_word.isalnum()):
                continue
            selected_words.append(a_word)
            counter += 1
    return selected_words

def get_inverse_filter_by_number(token_set,frequency_per_word,total_number):
    zipped = zip(token_set,frequency_per_word)
    zipped.sort(key = lambda t: t[1], reverse=True)
    selected_words = []
    for  i in range(len(zipped)):
        if i >= total_number:
            selected_words.append(zipped[i][0])
    return selected_words

def filter_by_set(all_documents_dict,set_of_words):
    final_dict = {}
    for key in all_documents_dict.keys():
        new_document = all_documents_dict[key]
        for word in set_of_words:
            # TODO: revisar porque no puedo sacar * y +
            if word in new_document:
                if word.isalnum():
                    try:
                        #patt = re.compile('(\s*)'+word+'(\s*)')
                        #new_document = patt.sub('', new_document)
                        new_document = re.sub(r'\b%s\b' % word, '', new_document)
                    except:
                        continue
        final_dict[key] = new_document
    return final_dict