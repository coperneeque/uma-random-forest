from ast import For
from cmath import nan
from csv import reader
from statistics import median

def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

def str_column_to_float(dataset, column):
	for row in dataset:
		try:
			row[column] = float(row[column].strip())
		except:
			print(row[column])
			# print()
			row[column] = nan

def clean_nans_float(dataset):
	"""Zastępuje brakujące wartości atrybutów medianami"""
	num_nans = 0
	num_attributes = len(dataset[0]) - 1  # ostatni to klasa
	medians = []
	# oblicz mediany wszystkich atrybutów:
	for i in range(num_attributes):
		attr_vals = []
		for row in dataset:
			attr_vals.append(row[i])
		medians.append(median(attr_vals))
	# podstaw mediany za nan-y:
	for i in range(num_attributes):
		for row in dataset:
			if row[i] is nan:
				num_nans += 1
				row[i] = medians[i]
	return num_nans

def clean_nans_labels(dataset):
	"""Usuwa przykłady z brakującymi wartościami atrybutów"""
	num_nans = 0
	num_attributes = len(dataset[0]) - 1  # ostatni to klasa
	# rows_to_del = []
	# print("Liczba atybutów %s" %num_attributes)
		# row_idx = 0
		# while row_idx < len(dataset):
		# 	row_idx += 1
	for row_idx in reversed(range(len(dataset))):
	# for row_idx in range(len(dataset)):
		for i in range(num_attributes):
			if dataset[row_idx][i] == "":
				# print(dataset[row_idx])
				# print(f"Długość przykładu (bez klasy):\n{len(dataset[row_idx]) - 1}")
				del dataset[row_idx]
				# rows_to_del.append(row_idx)
				num_nans += 1
				# row_idx -= 1  # trzeba powrócić do tego wiersza, bo po usunięciu następny się przesunął tutaj, gdzie ejsteśmy
	# del dataset[rows_to_del]
	return num_nans

def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup
