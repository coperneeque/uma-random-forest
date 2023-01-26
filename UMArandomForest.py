from random import seed
import sys


import DataFunctions as df
import RandomForest as rf
import Eval as e

if __name__ == "__main__":
	dataSetPath = sys.argv[1]
	datasetType = sys.argv[2]
	tournament_size = int(sys.argv[3])
	seed(2)
	# filename = dataSetPath
	dataset = df.load_csv(dataSetPath)
	if datasetType=="numeric":
		for i in range(0, len(dataset[0])-1):
			df.str_column_to_float(dataset, i)
		df.str_column_to_int(dataset, len(dataset[0])-1)
	elif datasetType!="discrete":
		sys.exit(1)
	n_folds = 5
	max_depth = 10
	min_size = 1
	# sample_size = 1.0
	for n_trees in [5, 10, 15]:
		scores = e.evaluate_algorithm(dataset, rf.random_forest, n_folds, max_depth, min_size, n_trees, tournament_size)
		print('Liczba drzew w lesie: %d' % n_trees)
		print('Poprawnosc prdykcji w kolejnych iteracjach: %s' % scores)
		print('Srednia poprawnosc predykcji: %.2f%%' % (sum(scores)/float(len(scores))))