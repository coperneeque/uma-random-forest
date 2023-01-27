from random import randrange
from random import choice
from random import sample
from scipy.stats import entropy
from collections import Counter
import numpy as np

def test_split(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right

def gini_index(groups, classes):
	n_instances = float(sum([len(group) for group in groups]))
	gini = 0.0
	for group in groups:
		size = float(len(group))
		if size == 0:
			continue
		score = 0.0
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		gini += (1.0 - score) * (size / n_instances)
	return gini

def info_gain(groups):
	left = groups[0]
	right = groups[1]
	classL = list()
	classR = list()
	for elem in left:
		classL.append(elem[-1])
	for elem in right:
		classR.append(elem[-1])
	classT = classL + classR
	prob = np.array(list(Counter(classT).values()))/len(classT)
	probL = np.array(list(Counter(classL).values()))/len(classL)
	probR = np.array(list(Counter(classR).values()))/len(classR)
	avg = (entropy(probL) + entropy(probR))/2
	return entropy(prob) - avg

def get_split_tournament(dataset, features, tournament_size):
	class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_groups = 999, 999, None
# 
	tests_l = list()
	for index in features:
		values_list = set()
		for row in dataset:
			values_list.add(row[index])
		values_list = list(values_list)
		for val in values_list:
			tests_l.append((index, val))
	print(len(tests_l))
	groups = None
	res_l = list()
	if tournament_size > 0:
		for i in range(tournament_size):
			if(len(tests_l)==0):
				break
			test = choice(tests_l)
			tests_l.remove(test)
			res_l.append((test[0], test[1], test_split(test[0], test[1], dataset)))
	else:
		for test in tests_l:
			res_l.append((test[0], test[1], test_split(test[0], test[1], dataset)))
	while len(res_l) > 1:
		test1, test2 = sample(res_l, 2)
		gini1 = gini_index(test1[2], class_values)
		gini2 = gini_index(test2[2], class_values)
		if gini1 < gini2:
			res_l.remove(test2)
			groups = test1[2]
		else:
			groups = test2[2]
			res_l.remove(test1)
	b_index, b_value, b_groups = res_l[0][0], res_l[0][1], groups
	return {'index':b_index, 'value':b_value, 'groups':b_groups}

def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)

def split(node, max_depth, min_size, features, depth, tournament_size):
	left, right = node['groups']
	del(node['groups'])
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)
		return
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split_tournament(left, features, tournament_size)
		split(node['left'], max_depth, min_size, features, depth+1, tournament_size)
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split_tournament(right, features, tournament_size)
		split(node['right'], max_depth, min_size, features, depth+1, tournament_size)

def build_tree(train, max_depth, min_size, features, tournament_size):
	root = get_split_tournament(train, features, tournament_size)
	split(root, max_depth, min_size, features, 1, tournament_size)
	return root

def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']

def bootstrap_sample(dataset):
	sample = list()
	while len(sample) < len(dataset):
		index = randrange(len(dataset))
		sample.append(dataset[index])
	return sample

def bagging_predict(trees, row):
	predictions = [predict(tree, row) for tree in trees]
	return max(set(predictions), key=predictions.count)

def random_forest(train, test, max_depth, min_size, n_trees, feature_size, tournament_size):
	trees = list()
	for i in range(n_trees):
		features = set()
		sample = bootstrap_sample(train)
		while len(features) < feature_size:
			index = randrange(len(sample[0])-1)
			features.add(index)
		tree = build_tree(sample, max_depth, min_size, features, tournament_size)
		trees.append(tree)
	predictions = [bagging_predict(trees, row) for row in test]
	return(predictions)
