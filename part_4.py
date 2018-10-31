import csv

savedPreferences = []
option = []

def overLord(variables, values):
	#updatePreferences(variables, values)

	searchRestaurant(variables, values)
	


def searchRestaurant(variables, values):
	# open csv file in read mode
	with open('restaurantinfo.csv', 'r') as csv_file:
		
		# creates an object
		csv_reader = csv.DictReader(csv_file)

		# find restaurants according to preferences
		global foundOption
		foundOption = findOptions(csv_reader, variables, values)

		generateAnswers(foundOption)
		


def findOptions(csv_reader, variables, values):
		# create list with possible options
		prospects = []

		# set flag if a option is found
		found = False
		
		for line in csv_reader:
			found = checkPreferences(line, variables, values)
			if(found):
				prospects.append(line)

		return prospects

def checkPreferences(line, variables, values):
		# minus one because array starts on 0...
		length = len(variables) - 1

		# check every variable
		while(0 <= length):
			if(line[variables[length]] == values[length]):
				length = length - 1
			else:	
				return False

		# print(line)
		return True

def generateAnswers(foundOption):
		numberOfOptions = len(foundOption)
		if  numberOfOptions== 0 :
			print('No options')
			setPreferencesToZero()
			main()
		elif numberOfOptions == 1:
			print('Found one!')
			global option
			option = foundOption
			#generateAnswer(foundOption)
		else:
			numberOfOptions = numberOfOptions - 1
			if 'pricerange' in variables and 'area' in variables and 'food' in variables:
				option = foundOption
			while(0 <= numberOfOptions):
				#print(foundOption[numberOfOptions]['restaurantname'])
				numberOfOptions = numberOfOptions - 1

def setPreferencesToZero():
	global savedPreferences
	savedPreferences = []
	global variables
	variables = []
	global values
	values = []

def updatePreferences(variables, values):
	global savedPreferences
	savedPreferences = savedPreferences.append('hej')

def generateQuestions():
	if 'pricerange'  not in variables:
		print('What pricerange?')
		test = input()
		variables.append('pricerange')
		if test != 'any':
			values.append(test)
	elif 'area' not in variables:
		print('What area?')
		test = input()
		variables.append('area')
		if test != 'any':
			values.append(test)
	elif 'food' not in variables:
		print('What food?')
		test = input()
		variables.append('food')
		if test != 'any':
			values.append(test)
	else:
		setPreferencesToZero()


def suggestFirstInList():
	print(foundOption[0])


def presentOption(option, variables, values):
	suggest = 'The ' + option['restaurantname'] + ' is a restaurant '
	iter = 0
	length = len(variables) - 1
	print(length)
	while(iter <= length):
		if 'pricerange' == variables[iter]:
			suggest = suggest + 'in the ' + values[iter] + ' price range '
			iter = iter + 1
		elif 'area' == variables[iter]:
			suggest = suggest + 'in the ' + values[iter] + ' part of town '
			iter = iter + 1
		elif 'food' == variables[iter]:
			suggest = suggest + 'and serves ' + values[iter] + ' food '
			iter = iter + 1
		else:
			iter = iter + 1
	print(suggest)

#def generateAnswer(foundOption):
#	length = len(variables) - 1
#	if(variables)


#variables = ['restaurantname', 'pricerange']
#values = ['prezzo', 'moderate']

#variables = ['food', 'area']
#values = ['indian', 'north']

#print('indian' in values)
#variables = ['pricerange']
#values = ['cheap']

#overLord(variables, values)

#variables = ['area', 'pricerange']
#values = ['west', 'moderate']

#print(savedPreferences)
#print(option)

variables = []
values = []

variables = ['restaurantname', 'pricerange', 'food', 'area']
values = ['prezzo', 'moderate', 'italian', 'west']

#overLord(variables, values)

#option = option[0]


#x = option["pricerange"]
#print(x)

variables = []
values = []

def main():
	global option


	variables = ['restaurantname', 'pricerange', 'food', 'area']
	values = ['prezzo', 'moderate', 'italian', 'west']

	print('Welcome what are you looking for?')
	input()
	overLord(variables, values)
	while(option == []):
		generateQuestions()
		overLord(variables, values)
	#check input''
	option = option[0]
	x = option
	print(x)
	presentOption(option, variables, values)
	print('Option ok?')
	answer = input()
	if answer == 'no':
		main()


main()



