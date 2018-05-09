# word_connection_matrix module

import numpy as np 
from sklearn.cluster import KMeans
from sklearn import svm

# -- Get word matrices --

def get_connective_matrix(document,bag_of_words):
	n_words = len(bag_of_words)
	connective_matrix = np.zeros((n_words,n_words))
	for line in document.splitlines():
		words_in_line = line.split()
		set_words_line = list(set(words_in_line))
		for word_i in set_words_line:
			word_i_index = words_in_line.index(word_i)
			if word_i in bag_of_words:
				i = bag_of_words.index(word_i)
				for word_j_index in range(len(words_in_line)):
					if word_j_index>word_i_index:
						word_j = words_in_line[word_j_index]
						if word_j in bag_of_words:
							if word_i != word_j:
								j = bag_of_words.index(word_j)
								connective_matrix[i,j] += 1
				connective_matrix[i,i] += words_in_line.count(word_i)
	return connective_matrix

def get_connective_matrix_phrases(document,bag_of_phrases):
	n_words = len(bag_of_phrases)
	connective_matrix = np.zeros((n_words,n_words))
	for line in document.splitlines():
		for word_i in bag_of_phrases:
			if word_i in line:
				word_i_index = line.index(word_i)
				i = bag_of_phrases.index(word_i)
				for word_j in bag_of_phrases:
					if word_j in line:
						word_j_index = line.index(word_j)
						if word_j_index>word_i_index:
							if word_i != word_j:
								j = bag_of_phrases.index(word_j)
								connective_matrix[i,j] += 1
				connective_matrix[i,i] += line.count(word_i)
	return connective_matrix

def get_matrices(documents,set_of_words):
	matrices = []
	names = []
	for key in documents.keys():
		matrices.append(get_connective_matrix(documents[key],set_of_words))
		names.append(key)
	return matrices,names

def get_matrices_phrases(documents,set_of_words):
	matrices = []
	names = []
	for key in documents.keys():
		matrices.append(get_connective_matrix_phrases(documents[key],set_of_words))
		names.append(key)
	return matrices,names

# -- Get word matrices --

def save_topic_conexion(connective_matrix,dict_words,a_word,another_word):
	a_topics = dict_words[a_word]
	another_topics = dict_words[another_word]
	for a_topic in a_topics:
		for another_topic in another_topics:
			connective_matrix[a_topic,another_topic] += 1

def get_topic_connective_matrix(document,dict_words,n_topics):
	topic_words = dict_words.keys()
	connective_matrix = np.zeros((n_topics,n_topics))
	for a_topic_word in topic_words:
		for line in document.splitlines():
			words_in_line = line.split()
			for w1_idx,a_word_in_line in enumerate(words_in_line):
				if a_word_in_line == a_topic_word or (len(a_topic_word) > 3 and a_word_in_line.startswith(a_topic_word) ):
					for w2_idx,another_word_in_line in enumerate(words_in_line):
						if w2_idx > w1_idx:
							for another_topic_word in topic_words:
								if another_word_in_line == another_topic_word or (len(another_topic_word) > 3 and another_word_in_line.startswith(another_topic_word)):
									save_topic_conexion(connective_matrix,dict_words,a_topic_word,another_topic_word)
	return connective_matrix
'''
def get_topic_connective_matrix(document,dict_words,n_topics):
	topic_words = dict_words.keys()
	n_words = len(topic_words)
	connective_matrix = np.zeros((n_topics,n_topics))

	for line in document.splitlines():
		words_in_line = line.split()
		set_words_line = list(set(words_in_line))
		for word_i_index in range(len(words_in_line)):
			word_i = words_in_line[word_i_index]
			for topic_word in topic_words:
				if topic_word
			# # # #
			if word_i in topic_words:
				for word_j_index in range(len(words_in_line)):
					word_j = words_in_line[word_j_index]
					if word_j_index>word_i_index and word_j in topic_words:
						for topic_i in dict_words[word_i]:
							for topic_j in dict_words[word_j]:
								connective_matrix[topic_i,topic_j] += 1
	return connective_matrix
'''
def get_topic_matrices(documents,dict_words,n_topics):
	matrices = []
	names = []
	for key in documents.keys():
		matrices.append(get_topic_connective_matrix(documents[key],dict_words,n_topics))
		names.append(key)
	return matrices,names


# -- Cluster matrices --

def get_kmeans_clusters(array_list,n_clusters):
	kmeans = KMeans(n_clusters=n_clusters,n_init=10, random_state=0)
	clusters = kmeans.fit(array_list)
	centers = clusters.cluster_centers_
	labels = clusters.labels_
	return centers,labels

def get_centroids(array_list,labels):
	labels_set = list(set(labels))
	count_totals = []
	centroids = []
	for i in labels_set:
		#count_totals.append(labels.count(i)*1.0)
		aux_array = []
		for j in range(len(labels)):
			if labels[j] == i:
				aux_array.append(array_list[j])
		centroids.append(np.divide(np.sum(aux_array,axis=0),labels.count(i)*1.0))
	return centroids

def get_svm_clusters(array_list):
	clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
	clf.fit(array_list)
	labels = clf.predict(array_list)
	return get_centroids(array_list,list(labels)),labels

def normalize_matrices(matrices_list,document_length):
	i = 0
	aux_list = []
	for doc in document_length.keys():
		aux_list.append(np.divide(matrices_list[i],round(document_length[doc],2)))
		i += 1
	return aux_list

# -- Working with unravel matrices --

def get_word_pairs(list_of_index,n_pairs,size_dict=300):
	unraveled_i,unraveled_j= np.unravel_index(list_of_index,(size_dict,size_dict))
	unraveled_without_diagonal = []
	for i in range(len(unraveled_i)):
		if unraveled_i[i]!=unraveled_j[i]:
			unraveled_without_diagonal.append((unraveled_i[i],unraveled_j[i]))
	return unraveled_without_diagonal[-n_pairs:]

def get_most_frequent_pairs(norm_array_list,n_pairs,size_dict=300):
	most_frequent = []
	for i in range(len(norm_array_list)):
		most_frequent.append(get_word_pairs(np.argsort(norm_array_list[i]),n_pairs,size_dict))
	return most_frequent

def check_symmetric(a, tol=1e-8):
    return np.allclose(a, a.T, atol=tol)

def to_tuple(matrix,z_c0,z_c1,z2_c0,z2_c1):
    a_matrix = matrix.as_matrix()
    words = matrix.columns
    a_tuple_list = []
    counter = 0
    for i in range(a_matrix.shape[0]):
        for j in range(a_matrix.shape[1]):
            a_tuple_list.append((words[i],words[j],a_matrix[i,j],str(z_c0[counter])+', ' +str(round(z2_c0[counter],2)),str(z_c1[counter])+' '+str(round(z2_c1[counter],2))))
            counter += 1
    return a_tuple_list