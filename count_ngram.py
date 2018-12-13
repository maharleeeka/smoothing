import re
from collections import Counter, defaultdict
from itertools import islice

path = 'test_data.txt'

test_data_file = open(path, 'r')
word_array = test_data_file.readlines();

i = 0;
new_dictionary = Counter(zip('', islice('', 1, None)))
word_frequency = Counter('');

while i < len(word_array):
	words = word_array[i]
	words = words.lower()
	words = words.replace('<s>', 'S')
	words = words.replace('</s>', '')
	words = re.findall("\w+", words)
	dictionary = Counter(zip(words, islice(words, 1, None)))
	word_frequency = word_frequency + Counter(words)
	new_dictionary = new_dictionary + dictionary
	i = i+1;

# print (new_dictionary) 
#new_dictionary - make a dictionary { bigram: count } i.e {('S', 'i'): 3, ... }

# print (word_frequency)  
#word_frequency - make a dictionary { word: count } i.r {'S': 3, 'i': 4 }

user_input = input("probability of: ")
user_input = 'S ' + user_input
user_input = re.findall("\w+", user_input) #needed to make a bigram of user_input

user_input_dictionary = Counter(zip(user_input, islice(user_input, 1, None))) 
# example input: i am human
# user_input_dictionary = { ('s', 'i'): 1, ('am', 'human'): 1 }

# looking_for_this_prob = user_input_dictionary.get(user_input[0], user_input[1])

k_value = float(input("k value: "))

j = 0
probability = 1

for key in user_input_dictionary:
	bigram_count = new_dictionary.get(key)
	count = word_frequency.get(user_input[j])
	print ('key: ', key, ' bigram_count:', bigram_count, ' count: ', count)
	if (bigram_count == None or count == None): 
		bigram_count = 0 
		bigram_count += float(k_value)
	else:
		bigram_count = bigram_count + float(k_value)
		
	if (k_value > 0):
		prob_each = bigram_count / (count + len(new_dictionary))
	else:
		prob_each = bigram_count / count

	probability = probability * prob_each
	j = j + 1

print ('len: ', len(new_dictionary))
print (probability)
