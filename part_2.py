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
text_classifier.evaluate(
    word_to_integer_converter.convert_list(test_utterances_list),
    speech_act_to_vector_converter.convert_list(test_speech_act_list)
)

# Wait for input
while True:
    user_text = input("Enter text to evaluate: ")
    predicted_vector = text_classifier.predict_speech_act(array([word_to_integer_converter.convert_line(user_text)]))
    print(argmax(predicted_vector))
    predicted_integer: int = argmax(predicted_vector)
    textual_speech_act = speech_act_to_vector_converter.convert_to_speech_act(predicted_integer)
    print(textual_speech_act)
