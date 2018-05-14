# -*- coding: utf-8 -*-
# visalization module for epistemic network analysis
import os 
import text_preprocessing as tp
import matplotlib.pyplot as plt, mpld3
import matplotlib.patches as mpatches

root_path = os.path.join("..","..","..")
data_path = os.path.join(root_path,'data')
by_grade_and_content = os.path.join(data_path,'textos_ulloa_by_grade_content')

dict_by_grade_and_content = tp.get_dict_files_with_grade_and_content(by_grade_and_content)

colors = {'cuarto':'#DD2C00','tercero':'#FFD600','segundo':'#00C853','primero':'#0091EA','octavo':'#6200EA','septimo':'#455A64'}

def scatter_plot_by_grade(x_values,y_values,label_x,label_y,labels,legend_location=None,fig=None,ax=None):
	if not ax:
		fig, ax = plt.subplots()
	ax.set_xlabel(label_x, labelpad=6,fontsize=16)
	ax.set_ylabel(label_y, labelpad=10,fontsize=16)
	for k in x_values.keys():
		a_label =labels[k]
		doc_code = k.split('_')[0]
		grade = dict_by_grade_and_content[doc_code]['grade']
		a_color = colors[grade]
		scatt = ax.scatter(x_values[k],y_values[k],c=a_color,marker='v')
		tooltips = mpld3.plugins.PointLabelTooltip(scatt, labels=[a_label])
		mpld3.plugins.connect(plt.gcf(), tooltips)
	# create legend manually
	patch_1 = mpatches.Patch(color='#DD2C00', label='12th')
	patch_2 = mpatches.Patch(color='#FFD600', label='11th')
	patch_3 = mpatches.Patch(color='#00C853', label='10th')
	patch_4 = mpatches.Patch(color='#0091EA', label='9th')
	patch_5 = mpatches.Patch(color='#6200EA', label='8th')
	patch_6 = mpatches.Patch(color='#455A64', label='7th')
	if legend_location:
		plt.legend(title='level',handles=[patch_1,patch_2,patch_3,patch_4,patch_5,patch_6],loc=legend_location)


def scatter_plot_by_grade_with_nodes(x_values,y_values,label_x,label_y,labels,legend_location=None,fig=None,ax=None):
	if not ax:
		fig, ax = plt.subplots()
	ax.set_xlabel(label_x, labelpad=6,fontsize=16)
	ax.set_ylabel(label_y, labelpad=10,fontsize=16)
	for k in x_values.keys():
		a_label =labels[k]
		doc_code = k.split('_')[0]
		grade = dict_by_grade_and_content[doc_code]['grade']
		a_color = colors[grade]
		scatt = ax.scatter(x_values[k],y_values[k],c=a_color,marker='v')
		tooltips = mpld3.plugins.PointLabelTooltip(scatt, labels=[a_label])
		mpld3.plugins.connect(plt.gcf(), tooltips)
	# create legend manually
	patch_1 = mpatches.Patch(color='#DD2C00', label='12th')
	patch_2 = mpatches.Patch(color='#FFD600', label='11th')
	patch_3 = mpatches.Patch(color='#00C853', label='10th')
	patch_4 = mpatches.Patch(color='#0091EA', label='9th')
	patch_5 = mpatches.Patch(color='#6200EA', label='8th')
	patch_6 = mpatches.Patch(color='#455A64', label='7th')
	if legend_location:
		plt.legend(title='level',handles=[patch_1,patch_2,patch_3,patch_4,patch_5,patch_6],loc=legend_location)
