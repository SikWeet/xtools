from datetime import datetime


class DateTimeUtils:
	"""
	Utility class for working with dates and times.
	"""

	@staticmethod
	def format_date(date: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
		"""
		Formats a date into a string according to the specified format.
		
		:param date: The datetime object to format.
		:param format_string: The format string to use for formatting.
		:return: The formatted date string.
		"""
		return date.strftime(format_string)

	@staticmethod
	def parse_date(date_string: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
		"""
		Parses a date string into a datetime object.
		
		:param date_string: The date string to parse.
		:param format_string: The format string to use for parsing.
		:return: The parsed datetime object.
		"""
		return datetime.strptime(date_string, format_string)

	@staticmethod
	def date_difference(date1: datetime, date2: datetime) -> int:
		"""
		Calculates the difference between two dates in days.
		
		:param date1: The first datetime object.
		:param date2: The second datetime object.
		:return: The difference between the two dates in days.
		"""
		return (date1 - date2).days
