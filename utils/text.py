class TextUtils:
	"""
	Utility class for text manipulation and analysis.
	"""

	@staticmethod
	def count_words(text: str) -> int:
		"""
		Counts the number of words in a text.

		:param text: The text to analyze.
		:return: The number of words in the text.
		"""
		return len(text.split())

	@staticmethod
	def count_characters(text: str) -> int:
		"""
		Counts the number of characters in a text (including spaces).

		:param text: The text to analyze.
		:return: The number of characters in the text.
		"""
		return len(text)

	@staticmethod
	def remove_punctuation(text: str) -> str:
		"""
		Removes all punctuation marks from the text.

		:param text: The text to clean.
		:return: The text with punctuation removed.
		"""
		return ''.join(char for char in text if char.isalnum() or char.isspace())

	@staticmethod
	def to_title_case(text: str) -> str:
		"""
		Converts the text to title case (first letter of each word capitalized).

		:param text: The text to convert.
		:return: The text in title case.
		"""
		return text.title()

	@staticmethod
	def reverse_string(text: str) -> str:
		"""
		Reverses the given string.

		:param text: The text to reverse.
		:return: The reversed string.
		"""
		return text[::-1]
