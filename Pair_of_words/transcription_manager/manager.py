# -*- coding: utf-8 -*-

from os import listdir,mkdir,getcwd
from os.path import isfile, join, isdir
import subprocess
import sys
import shutil


'''
manager.py se encarga de leer archivos de transcripciones de 
audio y agruparlas según metadatos como: nivel, materia o
contenido. Para lograr lo anterior se asume que en el path
data_path (textos_ulloa) se encuentran todas las trans_
cripciones de audios, cada una en una respectiva carpeta con
su nombre.

Al agrupar los textos según la clase seleccionada, los archivos
quedan el path clusters_ciae/output/textos_by_{clase}

'''
import os

clusters_path = 'C:\Users\CATALINA ESPINOZA\Documents\clusters ciae'
output_path = join(clusters_path,'output')

def export_transcription_by_class(from_path,clustering_name,dict_by_class):
	output_folder = 'textos_ulloa_by_' + clustering_name
	dest_path = join(output_path,output_folder)
	if not os.path.exists(dest_path):
		os.makedirs(dest_path)
	for transcription_class in dict_by_class.keys():
		class_file = transcription_class.rstrip() + '.txt'
		file_path = join(dest_path,class_file)
		final_file = open(file_path,'wb')
		for transcription in dict_by_class[transcription_class]:
			# leer cada archivo de la clase y copiar el texto en el archivo general
			transcription_file = transcription + '.txt'
			transcription_path = join(from_path,transcription,str(transcription_file))
			if os.path.exists(transcription_path):
				file_i = open(transcription_path,'r')
				for line in file_i:
					final_file.write(line)
				file_i.close()
				final_file.write('\n')
		final_file.close()
		if os.path.getsize(file_path) == 0:
			os.remove(file_path)

def export_transcription_by_class_in_folders(from_path,clustering_name,dict_by_class):
	output_folder = 'textos_ulloa_by_' + clustering_name
	dest_path = join(output_path,output_folder)
	if not os.path.exists(dest_path):
		os.makedirs(dest_path)
	for transcription_class in dict_by_class.keys():
		class_folder = join(dest_path,transcription_class.rstrip())
		if not os.path.exists(class_folder):
			os.makedirs(class_folder)
		class_file = transcription_class.rstrip() + '.txt'
		file_path = join(class_folder,class_file)
		final_file = open(file_path,'wb')
		for transcription in dict_by_class[transcription_class]:
			# leer cada archivo de la clase y copiar el texto en el archivo general
			transcription_file = transcription + '.txt'
			transcription_path = join(from_path,transcription,str(transcription_file))
			if os.path.exists(transcription_path):
				file_i = open(transcription_path,'r')
				for line in file_i:
					final_file.write(line)
				file_i.close()
				final_file.write('\n')
		final_file.close()
		if os.path.getsize(file_path) == 0:
			os.remove(file_path)