# -*- coding: utf-8 -*-
# text_preprocessing module for epistemic network analysis

import os
import sys
import matplotlib.pyplot as plt, mpld3

#--- Read Documents---

# Notese: Hay que seleccionar una funcion read_documents apropiada
# a la estructura del path donde se encuentran los archivos.

# read_documents: string -> {string: [string]}# lee los documentos contenidos en una carpeta
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

#--- Filter Documents---

def filter_by_duration(length_dict,text_dict,min_length=20):
    filtered_documents = {}
    for document in length_dict.keys():
        if length_dict[document] > min_length:
            filtered_documents[document] = text_dict[document]
    return filtered_documents

#--- Filter words per document ---


#--- Split documents ---
def split_excels(lines_dict,label_dict,period_length=10,overlap_length=5,n_seconds_per_line=5):
    documents_splitted = {}
    labels_splitted = {}
    for doc in lines_dict.keys():
        doc_text = lines_dict[doc]
        #doc_text = map(str,lines_dict[doc])
        
        n_lineas = len(doc_text)
        n_lineas_period = int((period_length*60)/n_seconds_per_line)# n lineas of a number of minutes
        n_lineas_overlap = int((overlap_length*60/n_seconds_per_line))

        shift = (n_lineas_period - n_lineas_overlap)

        iteration = 0
        i = 0
        j = 0
        while j + shift < n_lineas:
            
            i = iteration * shift
            j = i + n_lineas_period

            key_doc_splitted = doc+'_period_'+str(iteration)
            try:
                documents_splitted[key_doc_splitted] = '\n'.join(doc_text[i:j])
            except:
                print doc_text[i:j]
                raise
            labels_splitted[key_doc_splitted] = '_'.join(['period',str(iteration),label_dict[doc]])
            
            iteration += 1

        if (j + shift) - n_lineas < 0.3 * shift :
            key_doc_splitted = doc+'_period_'+str(iteration)
            documents_splitted[key_doc_splitted] = '\n'.join(doc_text[-n_lineas_period:])
            labels_splitted[key_doc_splitted] = '_'.join(['end',label_dict[doc]])
        else:
            labels_splitted[key_doc_splitted] = '_'.join(['end',label_dict[doc]])

    return documents_splitted,labels_splitted

def split_documents(text_dict,label_dict,period_length=10,overlap_length=5,n_seconds_per_line=5):
    documents_splitted = {}
    labels_splitted = {}
    for doc in text_dict.keys():
        doc_text = text_dict[doc].splitlines()
        
        n_lineas = len(doc_text)
        n_lineas_period = int((period_length*60)/n_seconds_per_line)# n lineas of a number of minutes
        n_lineas_overlap = int((overlap_length*60/n_seconds_per_line))

        shift = (n_lineas_period - n_lineas_overlap)

        iteration = 0
        i = 0
        j = 0
        while j + shift < n_lineas:
            
            i = iteration * shift
            j = i + n_lineas_period

            key_doc_splitted = doc+'_period_'+str(iteration)
            documents_splitted[key_doc_splitted] = '\n'.join(doc_text[i:j])
            labels_splitted[key_doc_splitted] = '_'.join(['period',str(iteration),label_dict[doc]])
            
            iteration += 1

        if (j + shift) - n_lineas < 0.3 * shift :
            key_doc_splitted = doc+'_period_'+str(iteration)
            documents_splitted[key_doc_splitted] = '\n'.join(doc_text[-n_lineas_period:])
            labels_splitted[key_doc_splitted] = '_'.join(['end',label_dict[doc]])
        else:
            labels_splitted[key_doc_splitted] = '_'.join(['end',label_dict[doc]])

    return documents_splitted,labels_splitted

def get_labels_and_splitted_documents_by_session(text_dict,label_dict,period_length=10,overlap_length=5,n_seconds_per_line=5):
    documents_splitted_by_session = {}
    labels_splitted_by_session = {}
    for doc in text_dict.keys():
        documents_splitted = {}
        labels_splitted = {}

        doc_text = text_dict[doc].splitlines()
        n_lineas = len(doc_text)
        n_lineas_period = int((period_length*60)/n_seconds_per_line)# n lineas of a number of minutes
        n_lineas_overlap = int((overlap_length*60/n_seconds_per_line))

        shift = (n_lineas_period - n_lineas_overlap)
        
        iteration = 0
        i = 0
        j = 0
        while j + shift < n_lineas:
            i = iteration * shift
            j = i + n_lineas_period
            key_doc_splitted = doc+'_period_'+str(iteration)
            documents_splitted[key_doc_splitted] = '\n'.join(doc_text[i:j])
            labels_splitted[key_doc_splitted] = '_'.join(['period',str(iteration),label_dict[doc]])
            iteration += 1
        
        if (j + shift) - n_lineas < 0.3 * shift :
            key_doc_splitted = doc+'_period_'+str(iteration)
            documents_splitted[key_doc_splitted] = '\n'.join(doc_text[-n_lineas_period:])
            labels_splitted[key_doc_splitted] = '_'.join(['end',label_dict[doc]])
        else:
            labels_splitted[key_doc_splitted] = '_'.join(['end',label_dict[doc]])

        documents_splitted_by_session[doc] = documents_splitted
        labels_splitted_by_session[doc] = labels_splitted

    return documents_splitted_by_session,labels_splitted_by_session

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

'''
def split_documents_in_acts(dict_doc,dict_length,minutes,overlap):
    documents_splitted = {}
    document_lengths = []
    labels = []
    for doc in dict_doc.keys():
        length = dict_length[doc]
        doc_text = dict_doc[doc].splitlines()
        n_lineas = len(doc_text)
        n_lineas_minutes = int((minutes*60)/5)# n lineas of a number of minutes
        n_lineas_overlap = int((overlap*60/5))
        n_etapas = int(n_lineas/overlap)
        
        inicio = doc_text[:n_lineas_minutes] # primeros 10m
        descenlace = doc_text[-n_lineas_minutes:] # ultimos 10m
        documents_splitted[doc] = {}
        documents_splitted[doc]['beginning'] = '\n'.join(inicio)
        documents_splitted[doc]['end'] = '\n'.join(descenlace)
        labels.append(doc+'_'+'beginning')
        
        iteration = 1
        i = 0
        j = 0
        while j<(n_lineas-n_lineas_minutes):
            i = iteration *(n_lineas_minutes-overlap)
            j = i + n_lineas_minutes
            documents_splitted[doc]['intermedio_'+str(iteration)] = '\n'.join(doc_text[i:j])
            labels.append(doc+'_'+'intermedio_'+str(iteration))
            iteration += 1
        labels.append(doc+'_'+'end')
        document_lengths += [n_lineas_minutes for i in range(iteration+1)]
    return documents_splitted,document_lengths,labels

def get_labels_and_splitted_documents(dict_labels,dict_text,dict_doc,minutes):
    documents_separated = {}
    labels = []
    for doc in dict_doc.keys():
        etapas = []
        etapas.append('beginning')
        for keys in dict_doc[doc].keys():
            if keys.startswith('intermedio'):
                etapas.append(keys)
        etapas.append('end')
        new_label = dict_labels[doc]['grade']+'_'+dict_labels[doc]['content']
        new_label = new_label.replace(' ','_')
        for i in range(len(etapas)):
            new_key = doc+'_'+etapas[i]
            documents_separated[new_key] = dict_doc[doc][etapas[i]]
            labels.append(new_key+'_'+new_label)
    return labels,documents_separated



def get_labels_and_splitted_documents_by_session(dict_labels,dict_text,dict_doc,minutes):
    set_dict = []
    set_labels = []
    for doc in dict_doc.keys():
        etapas = []
        etapas.append('beginning')
        for keys in dict_doc[doc].keys():
            if keys.startswith('intermedio'):
                etapas.append(keys)
        etapas.append('end')
        documents_separated = {}
        labels = []
        new_label = dict_labels[doc.split('_')[0]]['grade']+'_'+dict_labels[doc.split('_')[0]]['content']+'_'+ doc.split('_')[0]
        new_label = new_label.replace(' ','_')
        for i in range(len(etapas)):
            new_key = doc+'_'+etapas[i]
            documents_separated[new_key] = dict_doc[doc][etapas[i]]
            labels.append(new_key+'_'+new_label)
        set_labels.append(labels)
        set_dict.append(documents_separated)
    return set_labels,set_dict
'''