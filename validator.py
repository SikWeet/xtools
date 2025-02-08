import re
from datetime import datetime

class Validator:
	"""
	A class for validating different types of data.
	"""

	@staticmethod
	def is_email(value: str) -> bool:
		"""
		Checks if the string is a valid email.
		"""
		email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		return bool(re.match(email_regex, value))

	@staticmethod
	def is_phone(value: str) -> bool:
		"""
		Checks if the string is a valid phone number.
		Supports international numbers with a country code.
		"""
		phone_regex = r"^\+?[1-9]\d{1,14}$"
		return bool(re.match(phone_regex, value))

	@staticmethod
	def is_date(value: str, date_format: str = "%Y-%m-%d") -> bool:
		"""
		Checks if the string is a valid date in the given format.
		"""
		try:
			datetime.strptime(value, date_format)
			return True
		except ValueError:
			return False

	@staticmethod
	def is_url(value: str) -> bool:
		"""
		Checks if the string is a valid URL.
		"""
		url_regex = r"^(https?|ftp)://[^\s/$.?#].[^\s]*$"
		return bool(re.match(url_regex, value))

	@staticmethod
	def is_integer(value: str) -> bool:
		"""
		Checks if the string is a valid integer.
		"""
		return value.isdigit()

	@staticmethod
	def is_float(value: str) -> bool:
		"""
		Checks if the string is a valid floating point number.
		"""
		try:
			float(value)
			return True
		except ValueError:
			return False