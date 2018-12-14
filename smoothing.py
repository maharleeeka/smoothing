import re, csv
from functools import reduce
from collections import Counter, defaultdict
from itertools import islice

def main():
	print ("1. laplace bigram smoothing")
	print ("2. good turing n gram smoothing")

	choice = input("\nChoose: ")

	path = 'final.txt'

	test_data_file = open(path, 'r')
	word_array = test_data_file.readlines();

	i = 0;
	new_dictionary = Counter(zip('', islice('', 1, None)))
	word_frequency = Counter('');

	print ("\nprocessing your test data input...")

	while i < len(word_array):
		words = word_array[i]
		words = words.lower()
		words = re.findall("\w+", words)
		dictionary = Counter(zip(words, islice(words, 1, None)))
		word_frequency = word_frequency + Counter(words)
		new_dictionary = new_dictionary + dictionary
		i = i+1;

	user_input = input("\nenter phrase/sentence: ")
	user_input = user_input.lower()
	user_input_clean = re.findall("\w+", user_input)
	user_input_dictionary = Counter(zip(user_input_clean, islice(user_input_clean, 1, None))) 

	if (choice == '1'):
		result = laplace(new_dictionary, word_frequency, user_input_clean, user_input_dictionary)
	elif (choice == '2'):
		result = good_turing(new_dictionary, word_frequency, user_input_dictionary)
	else:
		quit()

	print ("\n\nP(", user_input, ") = ", result)


def laplace(new_dictionary, word_frequency, user_input, user_input_dictionary):
	k_value = float(input("enter k value: "))

	j = 0
	probability = 1

	for key in user_input_dictionary:
		bigram_count = new_dictionary.get(key)
		count = word_frequency.get(user_input[j])

		if (count == None and k_value == 0):
			probability = 0.0
			break

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

	write_outputs(new_dictionary, user_input_dictionary)

	return probability

def good_turing(new_dictionary, word_frequency, user_input_dictionary): 

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

	nc_array = []
	counts_array = []

	for key in all_keys:
		counts_array_value = all_keys[key]
		counts_array.append(counts_array_value)

	item_list = remove_duplicates(counts_array)
	item_list.sort()

	i = 0
	while i < len(item_list):
		nc = 0
		for key in all_keys:
			value = all_keys[key]
			if (value == item_list[i]):
				nc += 1

		nc_array.append(nc)
		i += 1

	summation = getSummation(nc_array)
	probabilities = getProbabilities(nc_array, summation)
	c_star = getCountStar(nc_array)
	c_star.append(probabilities[len(probabilities) - 1])
	p_star = getProbabilityStar(nc_array, c_star, summation)
	p_star.append(probabilities[len(probabilities) - 1])
	
	arr = []
	
	for key in user_input_dictionary:
		try:
			arr_value = all_keys[key]
		except KeyError:
			arr_value = -1
		
		arr.append(arr_value)

	estimates = []
	i = 0
	while i < len(arr):
		estimate = p_star[arr[i]] / nc_array[arr[i]]
		estimates.append(estimate)
		i += 1
	
	result = reduce(lambda x, y: x*y, estimates)

	write_outputs(new_dictionary, user_input_dictionary)

	return result


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
	while i < len(nc_array):
		probability = (nc_array[i] * i) / summation
		probabilities.append(probability)
		i += 1

	return probabilities

def getCountStar(nc_array):
	i = 0
	c_star = []
	while i < len(nc_array) - 1:
		c_star_value = (i + 1) * (nc_array[i + 1] / nc_array[i])
		c_star.append(c_star_value)
		i += 1

	return c_star

def getProbabilityStar(nc_array, c_star, summation):
	i = 0
	prob_star = []

	while i < (len(nc_array) - 1):
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

def remove_duplicates(values):
	output = []
	seen = set()
	for value in values:
		if value not in seen:
			output.append(value)
			seen.add(value)
	return output

def write_outputs(new_dictionary, user_input_dictionary):
	w = csv.writer(open("outputs/test_data_bigram.csv", "w"))
	print ("\nwriting to test_data_bigram...")
	for key, val in new_dictionary.items():
		w.writerow([key, val])

	print ("writing to input_bigram...")
	w = csv.writer(open("outputs/input_bigram.csv", "w"))
	for key, val in user_input_dictionary.items():
		w.writerow([key, val])

main()