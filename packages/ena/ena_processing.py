# -*- coding: utf-8 -*-
# ena_processing module for epistemic network analysis

import os
import numpy as np

def look_for_topic_score(a_dict,word,size):
    values = []
    the_keys = a_dict.keys()
    for key in the_keys:
        if word.startswith(key):
            values = a_dict[key]
            return values
    return np.zeros((1,size))

def get_sqrt_product_matrix(a_vector):
    size = len(a_vector)
    a_matrix = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            a_matrix[i,j] = np.sqrt(a_vector[i] * a_vector[j])
    return a_matrix

def get_co_occurrence(list_of_topic_words,list_of_topic_scores,msw,topic_score_word_dict):
    n_topics = len(list_of_topic_words)
    co_occurrance_matrix = np.zeros((n_topics,n_topics))
    words = (" ".join(msw)).split()
    msw_topic_score =  np.zeros((1,n_topics))
    for word in words:
        # each word is related to the 9 topics in some way
        msw_topic_score += look_for_topic_score(topic_score_word_dict,word,n_topics)
    adj_matrix = get_sqrt_product_matrix(msw_topic_score[0])
    return adj_matrix

def get_co_occurrence_matrices(text_dict,selected_t_words,selected_t_scores,topic_score_word_dict,msw_length=5):
	co_occurrence_matrices = {}
	labels_array_matrices = []
	n_topics = len(selected_t_scores)
	for document in text_dict.keys():
	    a_co_occurrence_matrix = np.zeros((n_topics,n_topics))
	    doc_lines = text_dict[document].splitlines()
	    for i in range(len(doc_lines)):
	        if i <= len(doc_lines)-msw_length:
	            j = i+msw_length
	            a_co_occurrence_matrix += get_co_occurrence(selected_t_words,selected_t_scores,doc_lines[i:j],topic_score_word_dict)
	    co_occurrence_matrices[document] = a_co_occurrence_matrix
	    labels_array_matrices.append(document)
	return co_occurrence_matrices,labels_array_matrices

def co_occurrence_matrix_to_vector(matrix,diagonal):
    size = int(matrix.shape[0])
    if diagonal:
        iu = np.triu_indices(size,0)
    else:
        iu = np.triu_indices(size,1)
    upper_matrix = matrix[iu]
    return upper_matrix.flatten()

def get_total_co_occurrence(a_dict_of_matrices):
    return np.sum(a_dict_of_matrices.values(),0)

def a_product(x,y):
    aux_matrix = np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            aux_matrix[i,j] = x[i]*y[j]
    return aux_matrix

def projection(a,b):
    return np.dot(a,b)*1.0/np.dot(b,b)

def norm_vectors(a_dict_of_vectors):
    a_dict_of_norm_vectors = {}
    for k, v in a_dict_of_vectors.items():
        a_dict_of_norm_vectors[k] = v / np.linalg.norm(v)
    return a_dict_of_norm_vectors

def get_n_stanzas_by_doc(a_doc_n_lines,stanza_size,shift):
    shift_lines = shift
    return (a_doc_n_lines-(stanza_size-1))/shift_lines

def get_n_stanzas_by_dict(a_dict_of_d_length,stanza_size,shift):
    a_dict = {}
    for k,v in a_dict_of_d_length.items():
        a_dict[k] = get_n_stanzas_by_doc(len(v.splitlines()),stanza_size,shift)
    #print stanza_size
    return a_dict

def norm_vectors_by_number(a_dict_of_vectors,a_number):
    a_dict_of_norm_vectors = {}
    for k, v in a_dict_of_vectors.items():
        a_dict_of_norm_vectors[k] = v / a_number*1.0
    return a_dict_of_norm_vectors

def norm_vectors_by_length(a_dict_of_vectors,a_dict_of_n_stanzas):
    a_dict_of_norm_vectors = {}
    for k, v in a_dict_of_vectors.items():
        a_dict_of_norm_vectors[k] = v / a_dict_of_n_stanzas[k]
    return a_dict_of_norm_vectors

def sub_vectors(a_dict_of_vectors,a_vector):
    a_dict_of_sub_vectors = {}
    for k, v in a_dict_of_vectors.items():
        a_dict_of_sub_vectors[k] = v - a_vector
    return a_dict_of_sub_vectors

def get_sum_of_components(a_matrix,a_group):
    the_sum = 0
    for i,component_i in enumerate(a_group):
        for j,component_j in enumerate(a_group):
            if i>=j:
                the_sum += a_matrix[component_i,component_j]
    return the_sum

def get_sum_of_pair_of_components(a_matrix,a_group,b_group):
    the_sum = 0
    for i,component_i in enumerate(a_group):
        for j,component_j in enumerate(b_group):
            the_sum += a_matrix[component_i,component_j]
    return the_sum

def get_aggregated_matrix(a_matrix,groups):
    the_super_matrix = np.zeros((len(groups),len(groups)))
    # por cada grupo i
    for i,group_i in enumerate(groups):
        # por cada grupo j
        for j,group_j in enumerate(groups):
            if i<j:
                the_super_matrix[i,j] = get_sum_of_pair_of_components(a_matrix,group_i,group_j)
        the_super_matrix[i,i] = get_sum_of_components(a_matrix,group_i)
    return the_super_matrix