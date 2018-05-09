import mpld3
from mpld3 import plugins
from mpld3.utils import get_id
import matplotlib.patches as mpatches
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import text_preprocessing as tp
import os
import numpy as np
import pandas as pd
from scipy import stats
from text_preprocessing import *
import holoviews as hv
import word_connection_matrix as wcm

hv.extension('bokeh')

root_path = 'C:\Users\CATALINA ESPINOZA\Documents\clusters ciae'
data_path = os.path.join(root_path,'data')
by_grade_and_content = os.path.join(data_path,'textos_ulloa_by_grade_content')

dict_by_grade_and_content = tp.get_dict_files_with_grade_and_content(by_grade_and_content)

colors = {'cuarto':'#DD2C00','tercero':'#FFD600','segundo':'#00C853','primero':'#0091EA','octavo':'#6200EA','septimo':'#455A64'}
colors_time = {'d_0':'#DD2C00','d_1':'#FFD600','d_2':'#00C853','d_3':'#0091EA','d_4':'#6200EA','other':'#455A64'}
colors_who = {'profesor':'#DD2C00','estudiante':'#FFD600','otro':'#00C853'}
colors_period = {'inicio':'#DD2C00','act_I':'#FFD600','act_II':'#00C853','descenlace':'#0091EA'}

def scatter_plot_by_grade_by_cluster(indicator_x,indicator_y,labels_clusters,xlabel,ylabel,name_objects,description_objects,legend_location=None,dict_by_grade_and_content=dict_by_grade_and_content,fig=None,ax=None):
	if not ax:
		fig, ax = plt.subplots()
	ax.set_xlabel(xlabel, labelpad=3)
	ax.set_ylabel(ylabel, labelpad=15)
	markers= map(lambda x: 's' if x == 0 else 'o',labels_clusters)
	colores = []
	markers = []
	colores_names = []
	for i in range(len(indicator_x)):
		grade = dict_by_grade_and_content[name_objects[i]]['grade']
		a_color = colors[grade]
		colores_names.append(grade)
		colores.append(a_color)
		if labels_clusters[i] > 0:
			a_marker = 's'
		else:
			a_marker = 'v'
		markers.append(a_marker)
		scatt = ax.scatter(indicator_x[i],indicator_y[i],c=a_color,marker=a_marker)
		tooltips = mpld3.plugins.PointLabelTooltip(scatt, labels=[description_objects[i]])
		mpld3.plugins.connect(plt.gcf(), tooltips)
	# create legend manually
	patch_1 = mpatches.Patch(color='#DD2C00', label='Cuarto medio')
	patch_2 = mpatches.Patch(color='#FFD600', label='Tercero medio')
	patch_3 = mpatches.Patch(color='#00C853', label='Segundo medio')
	patch_4 = mpatches.Patch(color='#0091EA', label='Primero medio')
	patch_5 = mpatches.Patch(color='#6200EA', label='Octavo')
	patch_6 = mpatches.Patch(color='#455A64', label='Septimo')
	if legend_location:
		plt.legend(handles=[patch_1,patch_2,patch_3,patch_4,patch_5,patch_6], loc=legend_location)

def get_time_session(time):
	time_text = time.split(':')
	if time_text[0] == '00':
		if time_text[1][0] == '0':
			return 'd_0'
		elif time_text[1][0] == '1':
			return 'd_1'
		elif time_text[1][0] == '2':
			return 'd_2'
		elif time_text[1][0] == '3':
			return 'd_3'
		elif time_text[1][0] == '4':
			return 'd_4'
		else:
			return 'other'
	else:
		return 'other'

def scatter_plot_by_time_by_cluster(indicator_x,indicator_y,labels_clusters,xlabel,ylabel,description_objects,legend_location):
	fig, ax = plt.subplots()
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	markers= map(lambda x: 's' if x == 0 else 'o',labels_clusters)
	colores = []
	markers = []
	colores_names = []
	for i in range(len(indicator_x)):
		init_time = description_objects[i].split('_')[1]
		a_color = colors_time[get_time_session(init_time)]
		colores_names.append(init_time)
		colores.append(a_color)
		if labels_clusters[i] > 0:
			a_marker = 's'
		else:
			a_marker = 'v'
		markers.append(a_marker)
		scatt = ax.scatter(indicator_x[i],indicator_y[i],c=a_color,marker=a_marker)
		tooltips = mpld3.plugins.PointLabelTooltip(scatt, labels=[description_objects[i]])
		mpld3.plugins.connect(plt.gcf(), tooltips)
	# create legend manually
	patch_1 = mpatches.Patch(color='#DD2C00', label='[0:10)')
	patch_2 = mpatches.Patch(color='#FFD600', label='[10:20)')
	patch_3 = mpatches.Patch(color='#00C853', label='[20:30)')
	patch_4 = mpatches.Patch(color='#0091EA', label='[30:40)')
	patch_5 = mpatches.Patch(color='#6200EA', label='[40:50)')
	patch_6 = mpatches.Patch(color='#455A64', label='other')
	if legend_location:
		plt.legend(handles=[patch_1,patch_2,patch_3,patch_4,patch_5,patch_6], loc=legend_location)

def get_period(a_label):
	label_splitted = a_label.split('_')
	if label_splitted[1] == 'act':
		return label_splitted[1] + '_' + label_splitted[2]
	return label_splitted[1]

def scatter_plot_by_period_by_cluster(indicator_x,indicator_y,labels_clusters,xlabel,ylabel,description_objects,legend_location):
	fig, ax = plt.subplots()
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	markers= map(lambda x: 's' if x == 0 else 'o',labels_clusters)
	colores = []
	markers = []
	colores_names = []
	for i in range(len(indicator_x)):
		period = get_period(description_objects[i])
		a_color = colors_period[period]
		colores_names.append(period)
		colores.append(a_color)
		if labels_clusters[i] > 0:
			a_marker = 's'
		else:
			a_marker = 'v'
		markers.append(a_marker)
		scatt = ax.scatter(indicator_x[i],indicator_y[i],c=a_color,marker=a_marker)
		tooltips = mpld3.plugins.PointLabelTooltip(scatt, labels=[description_objects[i]])
		mpld3.plugins.connect(plt.gcf(), tooltips)
	# create legend manually
	patch_1 = mpatches.Patch(color='#DD2C00', label='inicio')
	patch_2 = mpatches.Patch(color='#FFD600', label='act_I')
	patch_3 = mpatches.Patch(color='#00C853', label='act_II')
	patch_4 = mpatches.Patch(color='#0091EA', label='descenlace')
	if legend_location:
		plt.legend(handles=[patch_1,patch_2,patch_3,patch_4], loc=legend_location)

def get_who(to_who):
	if to_who != to_who:
		return 'otro'
	if to_who.startswith('al'):
		return 'estudiante'
	if to_who.startswith('prof') or to_who.endswith('profe'):
		return 'profesor'
	else:
		return 'otro'

def scatter_plot_by_who_by_cluster(indicator_x,indicator_y,labels_clusters,xlabel,ylabel,description_objects,legend_location):
	fig, ax = plt.subplots()
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	markers= map(lambda x: 's' if x == 0 else 'o',labels_clusters)
	colores = []
	markers = []
	colores_names = []
	for i in range(len(indicator_x)):
		who = description_objects[i].split('_')[3]
		a_color = colors_who[get_who(who)]
		colores_names.append(who)
		colores.append(a_color)
		if labels_clusters[i] > 0:
			a_marker = 's'
		else:
			a_marker = 'v'
		markers.append(a_marker)
		scatt = ax.scatter(indicator_x[i],indicator_y[i],c=a_color,marker=a_marker)
		tooltips = mpld3.plugins.PointLabelTooltip(scatt, labels=[description_objects[i]])
		mpld3.plugins.connect(plt.gcf(), tooltips)
	# create legend manually
	patch_1 = mpatches.Patch(color='#DD2C00', label='profesor')
	patch_2 = mpatches.Patch(color='#FFD600', label='estudiante')
	patch_3 = mpatches.Patch(color='#00C853', label='otro')
	if legend_location:
		plt.legend(handles=[patch_1,patch_2,patch_3], loc=legend_location)


def get_ks_matrix(labels_clusters,array_list,set_of_words = set_all):
	matrices_cluster1 = []
	matrices_cluster0 = []
	labels_clusters = map(lambda x: 1 if x>0 else 0,labels_clusters)
	for i in range(len(labels_clusters)):
		if labels_clusters[i]:
			matrices_cluster1.append(array_list[i])
		else:
			matrices_cluster0.append(array_list[i])        
	w_ij_cluster1 = np.transpose(matrices_cluster1)
	w_ij_cluster0 = np.transpose(matrices_cluster0)
	ks_ij_clusters_1_0 = []
	p_val_ks_ij_clusters_1_0 = []
	for i in range(len(w_ij_cluster0)):
		ks = stats.ks_2samp(w_ij_cluster0[i],w_ij_cluster1[i])
		ks_ij_clusters_1_0.append(ks[0])
		p_val_ks_ij_clusters_1_0.append(ks[1])
	ks_matrix = np.reshape(ks_ij_clusters_1_0,(len(set_of_words),len(set_of_words)))
	return ks_matrix,w_ij_cluster0,w_ij_cluster1

is_1 = lambda x : 1 if x>0 else 0

def ks_heatmap(ks_matrix,w_ij_cluster0,w_ij_cluster1,set_of_words = set_all):
	count_pair_c0 = map(lambda x: sum(map(is_1,x)),w_ij_cluster0)
	count_pair_c1 = map(lambda x: sum(map(is_1,x)),w_ij_cluster1)
	freq_pair_c0 = map(lambda x: sum(x),w_ij_cluster0)
	freq_pair_c1 = map(lambda x: sum(x),w_ij_cluster1)
	df = pd.DataFrame(ks_matrix)
	df.columns = map(lambda x: x.replace(" ",""),set_of_words)
	df.index =  map(lambda x: x.replace(" ",""),set_of_words)
	
	heatmap = hv.HeatMap(wcm.to_tuple(df,count_pair_c0,count_pair_c1,freq_pair_c0,freq_pair_c1),vdims=['KS','freq_in_documents_and_by_minute_cluster_0','freq_in_documents_and_by_minute_cluster_1'])
	return heatmap