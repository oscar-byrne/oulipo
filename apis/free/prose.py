import random
import logging
import re

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

from ..paid import Langdetecter


#TO DO:
#	> replace str.replace for removing punctuation with a re.sub that hits all non-standard ones
#	> count whitespace and reject prose if there is too much by proportion
#	> count uppercase characters and reject prose if there are too many by proportion

class ProseFinder(object):

	def __init__(self):
		self.logger = logging.getLogger("ProseFinder")

	def get_raw_book(self):
		while True:
			try:
				text = load_etext(random.randrange(46000)) #46000 is approximately size of gutenberg catalogue
			except ValueError: #in case of no download method for that text id
				pass
			else:
				return strip_headers(text)

	def get_raw_paragraph(self):
		text = self.get_raw_book()
		paragraphs = text.split("\n\n") 
		return paragraphs[len(paragraphs)//2]

	def is_useful_prose(self, text):
		is_english = Langdetecter().is_english(text.split(".")[0]) #check first sentence
		#too_much_uppercase
		#too_much_whitespace
		suitable_length = len(text) > 300 and len(text) < 2000
		self.logger.info("is english: {}; is suitable length: {}".format(is_english, suitable_length))
		return all([is_english, suitable_length,])

	def sanitize_text(self, text):
		text = text.replace("_", "").replace("*", "")	#remove non-standard punctuation
		text = re.sub("\[[^\]]*\] ", "", text)			#remove text contained in square brackets
		text = " ".join(text.split())					#remove unnecessary whitespace
		return text

	def get_paragraph(self):
		while True:
			paragraph = self.get_raw_paragraph()
			if self.is_useful_prose(paragraph):
				return self.sanitize_text(paragraph)
			else:
				pass


