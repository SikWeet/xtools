from datetime import datetime, timedelta
from typing import List
import pytz

class DateTime:
	"""
	Class for working with dates and times.
	"""

	def __init__(self, zone: str = 'Europe/Moscow'):
		self._result = None
		self._prev_result = None
		self._results = []
		self._zone = zone

	@property
	def results(self) -> List[datetime]:
		"""
		Return all results

		:return: List[datetime]
		"""
		return self._results

	@property
	def prev(self) -> datetime:
		"""
		Return previous result
		
		:return: datetime
		"""
		return self._prev_result

	@property
	def result(self) -> datetime:
		"""
		Return current result

		:return: datetime
		"""
		return self._result

	@result.setter
	def result(self, value):
		if self._result:
			self._prev_result = self._result
			self._results.append(self._prev_result)
		self._result = value

	def now(self) -> "DateTime":
		"""
		Get datetime now using timezone

		:return: self
		"""
		self.result = datetime.now(pytz.timezone(self._zone))
		return self

	def today(self) -> "DateTime":
		"""
		Get datetime today

		:return: self
		"""
		self.result = datetime.today()
		return self

	def __add__(self, other):
		if isinstance(other, timedelta):
			self.result = self.result + other
			return self
		return NotImplemented

	def __sub__(self, other):
		if isinstance(other, timedelta):
			self.result = self.result - other
			return self
		return NotImplemented

	def __iter__(self):
		return iter(self.results)

	def __eq__(self, value):
		if isinstance(value, datetime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) == value.replace(tzinfo=pytz.timezone(self._zone))
		if isinstance(value, DateTime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) == value.result.replace(tzinfo=pytz.timezone(self._zone))
		return NotImplemented

	def __ne__(self, value):
		if isinstance(value, datetime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) != value.replace(tzinfo=pytz.timezone(self._zone))
		if isinstance(value, DateTime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) != value.result.replace(tzinfo=pytz.timezone(self._zone))
		return NotImplemented
	
	def __lt__(self, value):
		if isinstance(value, datetime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) < value.replace(tzinfo=pytz.timezone(self._zone))
		if isinstance(value, DateTime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) < value.result.replace(tzinfo=pytz.timezone(self._zone))
		return NotImplemented
	
	def __le__(self, value):
		if isinstance(value, datetime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) <= value.replace(tzinfo=pytz.timezone(self._zone))
		if isinstance(value, DateTime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) <= value.result.replace(tzinfo=pytz.timezone(self._zone))
		return NotImplemented
	
	def __gt__(self, value):
		if isinstance(value, datetime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) > value.replace(tzinfo=pytz.timezone(self._zone))
		if isinstance(value, DateTime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) > value.result.replace(tzinfo=pytz.timezone(self._zone))
		return NotImplemented
	
	def __bool__(self):
		return self.result != None

	def __ge__(self, value):
		if isinstance(value, datetime):
			return self.result.replace(tzinfo=pytz.timezone(self._zone)) >= value.replace(tzinfo=pytz.timezone(self._zone))
		if isinstance(value, DateTime):
			return self.result.replace(pytz.timezone(self._zone)) >= value.result.replace(pytz.timezone(self._zone))
		return NotImplemented

	def __str__(self):
		return str(self.result)

	def __repr__(self):
		return repr(self.result)


class DateTimeUtils:
	"""
	Utility class for working with dates and times.
	"""

	@staticmethod
	def get_now(timezone: str = 'Europe/Moscow') -> datetime:
		"""
		Get datetime now using timezone (default is Moscow | +3H)

		:param timezone: The date in the selected time zone (default Moscow)

		:return: datetime
		"""

		return datetime.now(pytz.timezone(timezone))
	
	@staticmethod
	def get_today() -> datetime:
		"""
		Get datetime today

		:return: datetime
		"""

		return datetime.today()

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
	def diff_days(date1: datetime, date2: datetime) -> int:
		"""
		Calculates the difference between two dates in days.
		
		:param date1: The first datetime object.
		:param date2: The second datetime object.
		:return: The difference between the two dates in days.
		"""
		return (date1 - date2).days

	@staticmethod
	def diff_seconds(date1: datetime, date2: datetime) -> int:
		"""
		Calculates the difference between two dates in seconds.
		
		:param date1: The first datetime object.
		:param date2: The second datetime object.
		:return: The difference between the two dates in seconds.
		"""
		return (date1 - date2).seconds
	
	@staticmethod
	def time_ago(from_date: datetime, only_number: bool = False) -> str | int:
		"""
		Returns a human-readable string showing how much time has passed since a given date.

		:Formats:
		if only_number is True
		type only is justnow, minute, hour, month, year

		if only_number is False
		type only is '.. мин назад', '.. ч назад', '.. дн назад', '.. мес назад', '.. г назад'


		:param from_date: Datetime object from which to count.
		:param only_number: Return only in the format "integer_type" for example "1_hour"
		:return: String like "just now", "2 days ago", "1 month ago".
		:return: In the format "date_type" for example "3_day".
		"""
		now = datetime.now()
		delta = now - from_date

		seconds = delta.total_seconds()
		minutes = seconds // 60
		hours = minutes // 60
		days = delta.days
		months = days // 30
		years = days // 365

		if seconds < 60:
			if only_number:
				return "0_justnow"
			return "только что"
		elif minutes < 60:
			if only_number:
				return f"{int(minutes)}_minute"
			return f"{int(minutes)} мин назад"
		elif hours < 24:
			if only_number:
				return f"{int(hours)}_hour"
			return f"{int(hours)} ч назад"
		elif days < 30:
			if only_number:
				return f"{int(days)}_day"
			return f"{int(days)} дн назад"
		elif months < 12:
			if only_number:
				return f"{int(months)}_month"
			return f"{int(months)} мес назад"
		else:
			if only_number:
				return f"{int(years)}_year"
			return f"{int(years)} г назад"