import re
from functools import reduce
from collections import Counter, defaultdict
from itertools import islice

def main():
	print ("1. laplace bigram smoothing")
	print ("2. good turing n gram smoothing")
	print ("3. quit")

	choice = input("choose: ")

	path = 'test_data.txt'

	test_data_file = open(path, 'r')
	word_array = test_data_file.readlines();

	i = 0;
	new_dictionary = Counter(zip('', islice('', 1, None)))
	word_frequency = Counter('');

	while i < len(word_array):
		words = word_array[i]
		words = words.lower()
		# words = words.replace('<s>', 'S')
		# words = words.replace('</s>', '')
		words = re.findall("\w+", words)
		dictionary = Counter(zip(words, islice(words, 1, None)))
		word_frequency = word_frequency + Counter(words)
		new_dictionary = new_dictionary + dictionary
		i = i+1;

	word_input = input("probability of: ")

	if (choice == '1'):
		laplace(new_dictionary, word_frequency, word_input)
	elif (choice == '2'):
		good_turing(new_dictionary, word_frequency, word_input)
	else:
		quit()


def laplace(new_dictionary, word_frequency, user_input):
	# print (new_dictionary) 
	#new_dictionary - make a dictionary { bigram: count } i.e {('S', 'i'): 3, ... }

	# print (word_frequency)  
	#word_frequency - make a dictionary { word: count } i.r {'S': 3, 'i': 4 }
	user_input = re.findall("\w+", user_input) #needed to make a bigram of user_input

	user_input_dictionary = Counter(zip(user_input, islice(user_input, 1, None))) 
	# example input: i am human
	# user_input_dictionary = { ('s', 'i'): 1, ('am', 'human'): 1 }

	k_value = float(input("k value: "))

	j = 0
	probability = 1

	for key in user_input_dictionary:
		bigram_count = new_dictionary.get(key)
		count = word_frequency.get(user_input[j])
		print ('key: ', key, ' bigram_count:', bigram_count, ' count: ', count)
		if (bigram_count == None): 
			bigram_count = 0 
			bigram_count += float(k_value)
		else:
			bigram_count = bigram_count + float(k_value)
		
		if (count == None):
			count = 0

		if (k_value > 0):
			prob_each = bigram_count / (count + len(new_dictionary))
		else:
			prob_each = bigram_count / count

		probability = probability * prob_each
		j = j + 1

	# 
	print (probability)

def good_turing(new_dictionary, word_frequency, user_input): 
	user_input = re.findall("\w+", user_input) #needed to make a bigram of user_input
	user_input_dictionary = Counter(zip(user_input, islice(user_input, 1, None))) 


	distinct_words_list = word_frequency
	distinct_words = len(word_frequency)
	possible_word_pairs = distinct_words * distinct_words

	all_keys = dict()
	all_words = []

	for key in word_frequency:
		all_words.append(key)

	for key in word_frequency:
		i = 0
		while i < distinct_words:
			value = new_dictionary.get((key, all_words[i]))
			if (value == None):
				value = 0
			all_keys[(key, all_words[i])] = value
			i += 1

	# print(all_keys)

	nc_array = []
	counter = 0

	while True:
		nc = 0
		for key in all_keys:
			value = all_keys[key]
			if (value == counter):
				nc += 1

		nc_array.append(nc)
		counter += 1
		if (nc == 0):
			break

	# print(nc_array)
	summation = getSummation(nc_array)
	probabilities = getProbabilities(nc_array, summation)
	c_star = getCountStar(nc_array)
	c_star.append(probabilities[len(probabilities) - 1])
	p_star = getProbabilityStar(nc_array, c_star, summation)
	p_star.append(probabilities[len(probabilities) - 1])

	arr = []
	
	for key in user_input_dictionary:
		arr_value = all_keys[key]
		arr.append(arr_value)

	estimates = []
	i = 0
	while i < len(arr):
		estimate = p_star[arr[i]] / nc_array[arr[i]]
		estimates.append(estimate)
		i += 1
	
	result = reduce(lambda x, y: x*y, estimates)
	print (result)
	# print (c_star)
	# print (p_star)

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()

    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

def getProbabilities(nc_array, summation):
	i = 0

	probabilities = []
	while i < len(nc_array) - 1:
		probability = (nc_array[i] * i) / summation
		probabilities.append(probability)
		i += 1

	return probabilities

def getCountStar(nc_array):
	i = 0
	c_star = []
	while i < len(nc_array) - 2:
		c_star_value = (i + 1) * (nc_array[i + 1] / nc_array[i])
		c_star.append(c_star_value)
		i += 1

	return c_star

def getProbabilityStar(nc_array, c_star, summation):
	i = 0
	prob_star = []

	while i < (len(nc_array) - 2):
		prob_star_value = (nc_array[i] * c_star[i]) / summation
		prob_star.append(prob_star_value)
		i += 1
	
	return prob_star

def getSummation(nc_array): 
	i = 0
	summation = 0
	while i < len(nc_array):
		summation = summation + (i * nc_array[i])
		i += 1

	return summation

main()