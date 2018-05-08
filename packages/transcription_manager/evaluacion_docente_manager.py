# -*- coding: utf-8 -*-

import os
from os import listdir,mkdir,getcwd
from os.path import isfile, join, isdir
import subprocess
import sys
import shutil
import xlrd
import pandas as pd

clusters_path = 'C:\Users\CATALINA ESPINOZA\Documents\clusters ciae'
output_path = join(clusters_path,'output')
data_path = join(clusters_path,'data')

def read_transcriptions(path):
	transcription_list = []
	files_names = []
	for file in listdir(path):
		df = pd.read_excel(join(path,file),encoding='utf-8')
		df = df.dropna(axis=1, how='all')
		df = df.dropna(axis=0, thresh=2)
		transcription_list.append(df)
		files_names.append(file)
	return transcription_list,files_names

def check_all_have_who(df_list):
	checkers = []
	for df in df_list:
		try:
			if len(df['quien'].values) > 0:
				checkers.append(True)
			else:
				checkers.append(False)
		except KeyError:
			checkers.append(False)
	return checkers

def check_text(text):
	if text == text:
		return text.rstrip().lower()
	else:
		return text

def get_sessions_in_tuples(df_list):
	sessions = []
	for index,df in enumerate(df_list):
		try:
			inicio = str(df['inicio'].values[0])
		except KeyError:
			inicio = -1
		try:
			text = ''
			for i,element in enumerate(list(df['texto'].values)):
				if element == element:
					if type(element) == int or type(element) == float:
						text = text + str(element) + '. '
					else:
						text = text + str(element.encode('utf-8')) + '. '
		except KeyError:
			text = ""
		sessions.append((index,inicio,text))
	return sessions

def get_dialogs_in_tuples(df_list):
	sessions = []
	for index,df in enumerate(df_list):
		try:
			inicio = df['inicio'].values[0]
		except KeyError:
			inicio = -1
		try:
			who = df['quien'].values
		except KeyError:
			who = [""]
		try:
			to_whom = df['a_quien'].values
		except KeyError:
			to_whom = df['a quien'].values
		try:
			subject = df['contenido'].values
		except KeyError:
			subject = ["" for x in range(len(who))]
		try:
			type_of_speech = df['parlamento'].values
		except KeyError:
			type_of_speech = ["" for x in range(len(who))]
		try:
			text = df['texto'].values
		except KeyError:
			text = ["" for x in range(len(who))]
		for i in range(len(who)):
			sessions.append((str(index)+'_'+str(i),inicio,who[i],get_to_whom(check_text(to_whom[i])),get_type_of_speech(check_text(type_of_speech[i])),check_text(subject[i]),text[i]))
	return sessions

def get_text_teachers(df_list):
	text_list = []
	metadata_list = []
	error_counter = 0
	for index,df in enumerate(df_list):
		try:
			inicio = df['inicio'].values[0]
		except KeyError:
			inicio = -1
		try:
			who = df['quien'].values
		except KeyError:
			text_list.append([])
			metadata_list.append({'to_whom':[],'type_of_speech':[],'subject':[],'inicio':inicio})
			continue
		try:
			to_whom = df['a_quien'].values
		except KeyError:
			to_whom = df['a quien'].values
		try:
			text = df['texto'].values
		except KeyError:
			text = ["" for x in range(len(who))]
		try:
			subject = df['contenido'].values
		except KeyError:
			subject = ["" for x in range(len(who))]
		try:
			type_of_speech = df['parlamento'].values
		except KeyError:
			type_of_speech = ["" for x in range(len(who))]
		try:
			metadata = {'to_whom':[],'type_of_speech':[],'subject':[],'inicio':inicio}
			text_values = []
			for i,values in enumerate(who):
				if values != values:
					continue
				values = str(values).lower()
				if values.startswith('prof'):
					text_values.append(text[i])
					metadata['to_whom'].append(check_text(to_whom[i]))
					metadata['type_of_speech'].append(check_text(type_of_speech[i]))
					metadata['subject'].append(check_text(subject[i]))
			text_list.append(text_values)
			metadata_list.append(metadata)
		except:
			print index
			text_list.append([])
			metadata_list.append({'to_whom':[],'type_of_speech':[],'subject':[],'inicio':inicio})
	return text_list,metadata_list

def get_text_students(df_list):
	text_list = []
	metadata_list = []
	error_counter = 0
	for index,df in enumerate(df_list):
		try:
			inicio = df['inicio'].values[0]
		except KeyError:
			inicio = -1
		try:
			who = df['quien'].values
		except KeyError:
			text_list.append([])
			metadata_list.append({'to_whom':[],'type_of_speech':[],'subject':[],'inicio':inicio})
			continue
		try:
			to_whom = df['a_quien'].values
		except KeyError:
			to_whom = df['a quien'].values
		try:
			text = df['texto'].values
		except KeyError:
			text = ["" for x in range(len(who))]
		try:
			subject = df['contenido'].values
		except KeyError:
			subject = ["" for x in range(len(who))]
		try:
			type_of_speech = df['parlamento'].values
		except KeyError:
			type_of_speech = ["" for x in range(len(who))]
		try:
			metadata = {'to_whom':[],'type_of_speech':[],'subject':[],'inicio':inicio}
			text_values = []
			for i,values in enumerate(who):
				if values != values:
					continue
				values = str(values).lower()
				if values.startswith('alum'):
					text_values.append(text[i])
					metadata['to_whom'].append(check_text(to_whom[i]))
					metadata['type_of_speech'].append(check_text(type_of_speech[i]))
					metadata['subject'].append(check_text(subject[i]))
			text_list.append(text_values)
			metadata_list.append(metadata)
		except:
			text_list.append([])
			metadata_list.append({'to_whom':[],'type_of_speech':[],'subject':[],'inicio':inicio})
	return text_list,metadata_list

def get_to_whom(to_whom):
	if to_whom != to_whom:
		return to_whom
	if to_whom == 'a todos' or to_whom.startswith('tod') or to_whom == 'alumnos' or to_whom =='alumnas':
		return 'todos'
	if to_whom.startswith('al'):
		return 'estudiante'
	if to_whom.startswith('gru'):
		return 'grupo'
	if to_whom.startswith('prof') or to_whom.endswith('profe'):
		return 'profe'
	else:
		return to_whom

def get_type_of_speech(type_of_speech):
	if type_of_speech != type_of_speech:
		return type_of_speech
	if type_of_speech.startswith('afir') or type_of_speech.startswith('afri') or type_of_speech.startswith('firma'):
		return 'afirmacion'
	if type_of_speech.startswith('pregun'):
		return 'pregunta'
	if type_of_speech.startswith('resp') or type_of_speech.startswith('res') :
		return 'respuesta'
	else:
		return type_of_speech
def get_tuples(text_list,metadata_list):
	tuples = []
	for i,metadata in enumerate(metadata_list):
		for j,a_data in enumerate(metadata['to_whom']):
			inicio = metadata['inicio']
			a_quien = a_data
			type_of_speech = metadata['type_of_speech'][j]
			subject = metadata['subject'][j]
			text = text_list[i][j]
			tuples.append((inicio,get_to_whom(a_quien),get_type_of_speech(type_of_speech),subject,text))
	return tuples

