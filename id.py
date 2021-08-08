
"""
	File name: Id.py
	Author: Given Kibanza
	Date Created: 08/08/2021
	Date last modified: (check the github commit history) 
	Python Version: 3.9
	Description: The code is used to generate a fake South African 
			ID which would pass SA ID checks/validation. 
			This is intended to be used for testing purposes solely 
	Inspired by: https://github.com/Chris927/generate-sa-idnumbers
"""

"""
NOTE/NB:
Whoever uses this script does so at their own risk. Use wisely and take into consideration the South African POPI act.
"""

#some links:
# https://www.rexegg.com/regex-quickstart.html
# https://en.wikipedia.org/wiki/National_identification_number#South_Africa
# http://knowles.co.za/generating-south-african-id-numbers/
# https://github.com/Chris927/generate-sa-idnumbers
# https://en.wikipedia.org/wiki/Luhn_algorithm
# https://www.checkid.co.za/

import random
import datetime
import re

class RSA_ID:
	year = 1234
	month = 12
	day = 31
	min_age = 15
	age = 30
	citizenship = 0
	id = "0000000000000" 
	randomize = 0
	
	gender=0  #0 means male, 1 means female
	generatedId = ""
	sequence= "800"
	

	def __init__(self, year=-1, month=-1, day=-1, gender=-1, citizenship=0, randomize=0, min_age=15):
		self.year = year
		self.month = month
		self.day = day
		self.gender = gender
		self.age = datetime.datetime.now().year - self.year
		self.citizenship = citizenship
		self.randomize = randomize
		self.min_age = min_age

		#start creating an ID
		if (randomize):
			self.__randomize()
		self.__initSequence()
		self.__generateID()

	#this function is private
	#called internally to initialize random values for fields which have not been set
	def __randomize(self):
		if self.year==-1: self.year = random.randint(1900, datetime.datetime.now().year-self.min_age)
		if self.month==-1: self.month = random.randint(1, 12)
		if self.day==-1: self.day = random.randint(1, 30)
		if self.gender==-1: self.gender = random.randint(0,1)
		self.age = datetime.datetime.now().year - self.year
	
	def __pad(self, n, length=3):
		#private method declaration
		#this functions adds 0 padding to a number
		#ie. __pad(3) returns 003, __pad(99) returns 099, __pad(999) returns 999
		n = str(n)
		pad = "0" * length
		pad = pad[0 : len(pad)-len(n)] + n
		return pad

	#used to generate the ID
	def __generateID(self):
		#private method declaration
		#first checks if the details provided are suitable
		#otherwise throws an error

		if (self.citizenship in [0,1] and self.gender in [0, 1] and self.year>=1900 and self.month in range(1,13) and self.day in range(1,32) and self.age>= self.min_age and self.min_age>=1):
			#proceed
			id_parts = [
				str(self.year)[2:],
				self.__pad(self.month, length=2),
				self.__pad(self.day, length=2),
				str(random.randint(0,4)) if self.gender==1 else str(random.randint(0,4)),
				self.sequence,
				str(self.citizenship),
				'8'
			]
			print(id_parts)
			id_joined_withoutCheckDigit = "".join(id_parts)
			self.id = id_joined_withoutCheckDigit + str(self.__calculateCheckDigit(id_joined_withoutCheckDigit))
		else:
			raise Exception("Invalid details supplied. check that min-age>=1")

	#used to initialize the sequence field
	#sequence is a number from 000 to 999, of this format
	def __initSequence(self):
		#private method declaration
		#creates a sequence of numbers from 000 to 999, which are placeholders in an ID
		if (self.randomize):
			sequences = [self.__pad(x) for x in range(0, 1000)]
			self.sequence = random.choice(sequences)
		else:
			self.sequence = '800'

	#used to calculate the last digit of the id, which is a check digit
	def __calculateCheckDigit(self,id_str):
		#private method declaration
		#calculates the Lohn digit

		#author, Chris927, used the replace function in js: 
		#replace(/\D/g, '') to remove all characters that aren't a digit
		id_str = re.sub('[^0-9]','', id_str)
		digits = [int(x) for x in id_str]
		digits.reverse()
		checkSum = 0
		for i in range(len(digits)):
			d = digits[i]
			if (i % 2 ==0):
				d *= 2
				if (d>9):
					d-= 9
			checkSum+= d

		return checkSum * 9 % 10

	#public method declaration
	#used to create another id for the same details
	def regenerateId(self):
		self.randomize = 1
		self.__initSequence()
		self.__generateID()
		return self.id

	#returns age of user
	def getAge(self):
		return self.age

	#use checkid website to validate
	#returns user ID
	def getID(self):
		return self.id