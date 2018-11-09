import re
from Levenshtein.StringMatcher import StringMatcher as sm
import csv
import argparse
import os
import sys
import random
from math import floor
from numpy import array, argmax
from word_to_integer_converter import WordToIntegerConverter
from data_extractor import DataExtractor
from text_classifier import TextClassifier
from speech_act_to_vector_converter import SpeechActToVectorConverter
from string import Template

from sentence_to_node_converter import SentenceToNodeConverter
from sentence_tree_builder import SentenceTreeBuilder
from variable_extractor import VariableExtractor


suggestions = []
found = False
loop = 0
variables = []
values = []

# Get parameters for the data extraction
parser = argparse.ArgumentParser()
parser.add_argument("--dstc2_dir", "-d",
                    help="Directory of the extracted tar.gz",
                    type=str,
                    default=os.getcwd())
parser.add_argument("--out", "-o",
                    help="Directory for the dialogues json file",
                    type=str,
                    default=os.getcwd())
args = parser.parse_args()
cwd = args.dstc2_dir
out_cwd = args.out
if not os.path.isdir(cwd):
    sys.exit("The dstc2_dir was not a dir. Please check your variables and try again!")
if not os.path.isdir(out_cwd):
    sys.exit("The out path was not a dir. Please check your variables and try again!")


# Fetch utterances and speech acts from json files
data_extractor = DataExtractor(cwd, out_cwd)
utterances = data_extractor.utterances

# Shuffle utterances randomly
utterances_list = list(map(tuple, utterances.items()))
random.shuffle(utterances_list)

# Split utterances into training and test data
split_on = floor(len(utterances)*0.85)
training_utterances = dict(utterances_list[:split_on])
test_utterances = dict(utterances_list[split_on+1:])

# Separated training data
training_utterances_list = list(training_utterances.keys())
training_speech_act_list = list(training_utterances.values())

# Separated test data
test_utterances_list = list(test_utterances.keys())
test_speech_act_list = list(test_utterances.values())

# Set sequence length
sequence_length = 25

# Initialise word_to_integer_converter
word_to_integer_converter = WordToIntegerConverter(training_utterances_list, sequence_length=sequence_length)

# Set vocabulary_size
vocabulary_size = len(word_to_integer_converter.word_to_int_dict) + 2

# Initialise the text classifier
text_classifier = TextClassifier(vocabulary_size=vocabulary_size, sequence_length=sequence_length)

# Initialise the speech act to vector converter
speech_act_to_vector_converter = SpeechActToVectorConverter()

# Train the text classifier
text_classifier.train(
    word_to_integer_converter.convert_list(training_utterances_list),
    speech_act_to_vector_converter.convert_list(training_speech_act_list)
)

# Test the classifier
loss, acc = text_classifier.evaluate(
    word_to_integer_converter.convert_list(test_utterances_list),
    speech_act_to_vector_converter.convert_list(test_speech_act_list)
)
print("Test loss: " + '{:.2f}'.format(loss))
print("Test accuracy: " + '{:.2f}'.format(acc))


def remove_brackets(word):
    return_word = word
    
    if return_word[0] == "(":
        return_word = return_word[1::]
    if return_word[(len(return_word) - 1)] == ")":
        return_word = return_word[:-1]
    
    return return_word

##============================================================

def searchRestaurant(variables, values):
    # open csv file in read mode
    with open('restaurantinfo.csv', 'r') as csv_file:
        
        # creates an object
        csv_reader = csv.DictReader(csv_file)

        # find restaurants according to preferences
        global suggestions
        suggestions = findOptions(csv_reader, variables, values)
        generateAnswers()
        csv_file.close()

# create list with possible options
def findOptions(csv_reader, variables, values):
        prospects = []
        for line in csv_reader:
            if(checkPreferences(line, variables, values)):
                prospects.append(line)     
        return prospects

def checkPreferences(line, variables, values):
        # minus one because array starts on 0...
        length = len(variables) - 1
        if(len(variables) != len(values)):
                print('Sorry, no restaurant could be found accoring to preferences.')
                setPreferencesToZero()
                main()
        # check every variable
        while(0 <= length):
            if(values[length] == 'any'):
                length = length - 1
            elif(line[variables[length]] == values[length]):
                length = length - 1
            else:   
                return False
        return True

def generateAnswers():
        global found
        global loop
        global suggestions
        numberOfOptions = len(suggestions)
        if  numberOfOptions== 0 :
            setPreferencesToZero()
            loop = loop + 1
            main()
        elif numberOfOptions <= 3:
            found = True
        elif 'pricerange' in variables and 'area' in variables and 'food' in variables:
            found = True

def setPreferencesToZero():
    global variables
    variables = []
    global values
    values = []
    global suggestions
    suggestions = []
    global found
    found = False

def generateQuestions():
    global found
    global values
    global variables
    global loop
    if('pricerange'  not in variables and 'area' not in variables and 'food' not in variables):
        greeting = generateGreeting(loop)
        what = 'any'
        setQuestion(greeting,what)
        greeting = ''
    if 'pricerange'  not in variables and not found:
        greeting = 'What price range? \n'
        what = 'pricerange'
        setQuestion(greeting,what)
    if 'area' not in variables and not found:
        greeting = 'What area? \n'
        what = 'area'
        setQuestion(greeting,what)
    if 'food' not in variables and not found:
        greeting = 'What food? \n'
        what = 'food'
        setQuestion(greeting,what)

def setQuestion(message, what):
    global found
    global values
    global variables
    flag = False
    while(not flag):
        user_text = input(message)
        user_text = user_text.lower()
        speech_act = classifier(user_text)
        if(speech_act == 'thankyou'):
            print('Goodbye!')
            sys.exit()
        if(speech_act == 'inform'):
            flag = findVariablesAndTypes(user_text, variables, values, what)
    searchRestaurant(variables, values)


def templates(suggestions, variables, values):

    restaurant_templates = [Template('$restaurant is a great restaurant'), Template('$restaurant is a nice restaurant'), Template('$restaurant is a restaurant')]
    food_temp = Template('serving $food food')
    area_temp = Template('in the $area part of town')
    pricerange_temp = Template('in the $pricerange price range')

    i = random.randint(0,2)
    restaurant_templates = restaurant_templates[i]
    
    dictionary ={'restaurant':suggestions['restaurantname'], 'food':suggestions['food'], 'area':suggestions['area'], 'pricerange':suggestions['pricerange']}

    restaurant_templates = restaurant_templates.substitute(dictionary)
    food_temp = food_temp.substitute(dictionary)
    area_temp = area_temp.substitute(dictionary)
    pricerange_temp = pricerange_temp.substitute(dictionary)
    
    order = {'food': food_temp, 'area': area_temp, 'pricerange': pricerange_temp}

    length = len(variables) - 1
    i = 0
    word = 'first'
    new = []
    while i <= length:
        new.append(order[variables[i]])    #variable[0]
        i = i +1

    if length == 0:
        src = Template('$restaurant $first.')
        dictionary['first'] = new[0]
    elif length == 1:
        src = Template('$restaurant $first and it is $second.')
        dictionary['first'] = new[0]
        dictionary['second'] = new[1]
    elif length == 2:
        src = Template('$restaurant $first and it is $second $third.')
        dictionary['first'] = new[0]
        dictionary['second'] = new[1]
        dictionary['third'] = new[2]
    
    dictionary['restaurant'] = restaurant_templates

    #print(src.substitute(dictionary))

def findVariablesAndTypes(user_text, variables, values, type):

    root_node = None
    nodes_list = None
    
    nodes_list = SentenceToNodeConverter().build_node_list(user_text)
    root_node = SentenceTreeBuilder().build_tree(nodes_list)
    variable_nodes = dict()

    root_node.print()
    variable_extractor = VariableExtractor()
    variable_extractor.traverse_tree(root_node)
    variable_extractor.search_for_variables_in_tree(root_node)
    variable_extractor.search_for_variable_without_tree(nodes_list)
    
    for key, value in variable_extractor.variable_nodes.items():
        value.variable_print()
    return checkValidity(user_text, variables, values, type, variable_extractor.variable_nodes)


def checkValidity(user_text, variables, values, type, variable_nodes):
    #global variable_nodes
    if(not variable_nodes.items()):
        return False

    flag = False
    for key, value in variable_nodes.items():
        if key == type or type == 'any':
            flag = True

    if flag:
        for key, value in variable_nodes.items():
            if(key == type or 'any' == type):
                variables.append(key)
                values.append(value.text)
            elif not (type != key and value.text == 'any'):
                if key in variables:
                    index = variables.index(key)
                    del variables[index]
                    del values[index]
                variables.append(key)
                values.append(value.text)
        return True
    else:
        return False

def classifier(user_text):

    predicted_vector = text_classifier.predict_speech_act(array([word_to_integer_converter.convert_line(user_text)]))
    predicted_integer: int = argmax(predicted_vector)
    textual_speech_act = speech_act_to_vector_converter.convert_to_speech_act(predicted_integer)
    return textual_speech_act

def generateGreeting(loop):
    if(loop == 0):
        greeting = "Welcome, what kind of restaurant are you looking for? \n"
    elif(loop == 100):
        greeting = "Sorry there are no more restaurants that match your preferences. Please state new preferences. \n"
    else:
        greeting = "Sorry, no restaurants match your preferences. Change your preferences please! \n"
    return greeting

def makeSuggestions():
    global suggestions
    global variables
    global values
    global found
    global loop
    speech_act = 'negate'
    i = 0
    length = len(suggestions) - 1
    while speech_act == 'negate' and i <= length:
        templates(suggestions[i], variables, values)
        user_text = input('Does that sound good?\n')
        user_text = user_text.lower()
        speech_act = classifier(user_text)
        temp = suggestions[i]
        i = i + 1
    if(speech_act == 'negate'):
        setPreferencesToZero()
        loop = 100
        main()
    suggestions = temp

def giveInformation():
    #global loop
    message = 'Would you like any more information? \n'
    user_text = input(message)
    user_text = user_text.lower()
    speech_act = classifier(user_text)
    if(speech_act == 'request' or speech_act == 'reqalts'):
        print('The ' + suggestions['restaurantname'] + ' address is ' + suggestions["addr"] + ', ' + suggestions["postcode"] + ' and it has telephone number ' + suggestions['phone'])
    print('Bye!')
    setPreferencesToZero()
    loop = 0
    main()

def main():
        global suggestions
        global variables
        global values
        global found
        global loop

        while(not found):
            generateQuestions()

        makeSuggestions()
       
        giveInformation()

main()

