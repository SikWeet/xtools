class UnitConverter:
	"""
	Utility class for unit conversions.
	"""

	@staticmethod
	def celsius_to_fahrenheit(celsius: float) -> float:
		"""
		Converts Celsius to Fahrenheit.

		:param celsius: The temperature in Celsius.
		:return: The temperature in Fahrenheit.
		"""
		return celsius * 9/5 + 32

	@staticmethod
	def fahrenheit_to_celsius(fahrenheit: float) -> float:
		"""
		Converts Fahrenheit to Celsius.

		:param fahrenheit: The temperature in Fahrenheit.
		:return: The temperature in Celsius.
		"""
		return (fahrenheit - 32) * 5/9

	@staticmethod
	def meters_to_kilometers(meters: float) -> float:
		"""
		Converts meters to kilometers.

		:param meters: The distance in meters.
		:return: The distance in kilometers.
		"""
		return meters / 1000

	@staticmethod
	def kilometers_to_meters(kilometers: float) -> float:
		"""
		Converts kilometers to meters.

		:param kilometers: The distance in kilometers.
		:return: The distance in meters.
		"""
		return kilometers * 1000

	@staticmethod
	def grams_to_kilograms(grams: float) -> float:
		"""
		Converts grams to kilograms.

		:param grams: The mass in grams.
		:return: The mass in kilograms.
		"""
		return grams / 1000

	@staticmethod
	def kilograms_to_grams(kilograms: float) -> float:
		"""
		Converts kilograms to grams.

		:param kilograms: The mass in kilograms.
		:return: The mass in grams.
		"""
		return kilograms * 1000
