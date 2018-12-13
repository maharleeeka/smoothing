import re
from collections import Counter, defaultdict
from itertools import islice

word_array = [
	"S i am a human",
	"S i am not a stone",
	"S i i live in lahone"
];

i = 0;
new_dictionary = Counter(zip('', islice('', 1, None)))
word_frequency = Counter('');

while i < len(word_array):
	words = re.findall("\w+", word_array[i])
	dictionary = Counter(zip(words, islice(words, 1, None)))
	word_frequency = word_frequency + Counter(words)
	new_dictionary = new_dictionary + dictionary
	i = i+1;

print (new_dictionary) 
#new_dictionary - make a dictionary { bigram: count } i.e {('S', 'i'): 3, ... }

print (word_frequency)  
#word_frequency - make a dictionary { word: count } i.r {'S': 3, 'i': 4 }

user_input = input("probability of: ")
user_input = 'S ' + user_input
user_input = re.findall("\w+", user_input) #needed to make a bigram of user_input

user_input_dictionary = Counter(zip(user_input, islice(user_input, 1, None))) 
# example input: i am human
# user_input_dictionary = { ('s', 'i'): 1, ('am', 'human'): 1 }

# looking_for_this_prob = user_input_dictionary.get(user_input[0], user_input[1])

k_value = input("k value: ")

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
		
	prob_each = bigram_count / (count + len(new_dictionary))
	probability = probability * prob_each
	j = j + 1

print (probability)
