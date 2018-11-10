import re
from numpy import array


class WordToIntegerConverter:

    word_to_int_dict = dict()

    def __init__(self, training_vocabulary: list, vocabulary_size: int=None, sequence_length=100):
        #print("Initialising word to int dict")
        self.sequence_length = sequence_length
        self._setup(training_vocabulary, vocabulary_size)
        #print("Done initialising word to int dict")

    def _setup(self, training_vocabulary: list, vocabulary_size: int=None):
        # Count words in the text
        words_with_counter = dict()
        #print("Normalising text")
        text_as_list_stem = self.normalise_text(self.list_to_str(training_vocabulary))
        #print("Counting words")
        for word in text_as_list_stem:
            if word not in words_with_counter:
                words_with_counter[word] = 1
            else:
                words_with_counter[word] += 1
        # Organise the dict based on the counter in descending order
        #print("Sorting dict")
        sorted_dict = sorted(words_with_counter.items(), key=lambda kv: kv[1])
        sorted_dict.reverse()
        # Add words to word_to_int_dict based in the occurrence count for the words
        #print("Creating conversion dict")
        i = 2
        for word, count in sorted_dict:
            self.word_to_int_dict[word] = i
            # Break if the index exceeds the vocabulary size
            if vocabulary_size and i-1 is vocabulary_size:
                break
            i += 1

    @staticmethod
    def list_to_str(text_list: list):
        text_str = ""
        for text in text_list:
            text_str += text + " "
        text_str = text_str[:-1]
        return text_str

    @staticmethod
    def normalise_text(text: str):
        # Make text lower case
        text = text.lower()
        # Turns words into their stem form
        # Remove characters from string to standardise the strings
        re.sub('[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '', text)
        # Turn the string into a list of words
        text_as_list = text.split(" ")
        return text_as_list

    def convert_word(self, word: str):
        # If the word does not exist return 0
        if word not in self.word_to_int_dict:
            return 0
        # Convert the word using the dict
        converted_word = self.word_to_int_dict[word]
        return converted_word

    def convert_line(self, text: str):
        # Make sure the text is normalised such that the special chars are removed and words are turned into their stem
        text_as_list_stem = self.normalise_text(text)
        # Convert the stems of the words into integers using the setup dict
        text_as_integers = list()
        for word in text_as_list_stem:
            text_as_integers.append(self.convert_word(word))
        # Return an empty list if more than 100 integers exist
        if len(text_as_integers) > self.sequence_length:
            return array([])
        # Fill up the list with padding till it is 100 characters long
        for i in range(0, self.sequence_length - len(text_as_integers)):
            text_as_integers.append(1)
        return array(text_as_integers)

    def convert_list(self, text_list: list):
        #print("Converting word list")
        new_list = list()
        for line in text_list:
            converted_line = self.convert_line(line)
            if len(converted_line) > 0:
                new_list.append(converted_line)
        #print("Done converting word list")
        return array(new_list)
