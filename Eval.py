from random import randrange

def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split

def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0

# def get_confusion_matrix(actual, predicted):
# 	assert len(actual) == len(predicted)
# 	cm = []
# 	tp, fn, fp, tn = 0, 0, 0, 0
# 	#        predicted
# 	#         P    N
# 	#  a    +----+----+
# 	#  c  P | TP | FN |
# 	#  t    +----+----+
# 	#  u  N | FP | TN |
# 	#  a    +----+----+
# 	#  l

# 	for i in range(len(actual)):
# 		if actual[i] == predicted[i]:
# 			tp = 0

# 	return cm

def evaluate_algorithm(dataset, algorithm, n_folds, *args):
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = algorithm(train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		accuracy = accuracy_metric(actual, predicted)
		scores.append(accuracy)
	return scores
