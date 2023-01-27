#! /usr/bin/env python3

from random import seed
from math import sqrt
import sys

import DataFunctions as df
import RandomForest as rf
import Eval as e

if __name__ == "__main__":
	dataSetPath = sys.argv[1]
	datasetType = sys.argv[2]
	seed(None)
	dataset = df.load_csv(dataSetPath)
	if datasetType=="numeric":
		for i in range(0, len(dataset[0])-1):
			df.str_column_to_float(dataset, i)
		df.str_column_to_int(dataset, len(dataset[0])-1)
	elif datasetType!="discrete":
		sys.exit(1)
	num_nans = df.clean_nans(dataset)
	print(f"Uzupełniono {num_nans} brakujących wartości.")
	# sys.exit()
	n_folds = 5
	max_depth = 7
	min_size = 1
	feature_size = int(2*sqrt(len(dataset[0])-1))
	tournament_size = 0
	for n_trees in [5,15,25,50]:
	# for n_trees in [5]:
		scores = e.evaluate_algorithm(dataset, rf.random_forest, n_folds, max_depth, min_size, n_trees, feature_size, tournament_size)
		print('Liczba drzew w lesie: %d' % n_trees)
		print('Poprawnosc prdykcji w kolejnych iteracjach: %s' % scores)
		print('Srednia poprawnosc predykcji: %.2f%%' % (sum(scores)/float(len(scores))))