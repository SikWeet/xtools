import math

class MathUtils:
	"""
	Utility class for mathematical calculations.
	"""

	@staticmethod
	def factorial(n: int) -> int:
		"""
		Calculates the factorial of a number.

		:param n: The number to calculate the factorial of.
		:return: The factorial of the number.
		"""
		return math.factorial(n)

	@staticmethod
	def distance(x1: float, y1: float, x2: float, y2: float) -> float:
		"""
		Calculates the Euclidean distance between two points.

		:param x1, y1: Coordinates of the first point.
		:param x2, y2: Coordinates of the second point.
		:return: The distance between the points.
		"""
		return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

	@staticmethod
	def round_to_nearest(number: float, nearest: int) -> float:
		"""
		Rounds a number to the nearest multiple of a given value.

		:param number: The number to round.
		:param nearest: The nearest multiple to round to.
		:return: The rounded number.
		"""
		return round(number / nearest) * nearest

	@staticmethod
	def power(base: float, exponent: float) -> float:
		"""
		Calculates the power of a number.

		:param base: The base number.
		:param exponent: The exponent.
		:return: The result of base raised to the power of exponent.
		"""
		return math.pow(base, exponent)

	@staticmethod
	def is_prime(n: int) -> bool:
		"""
		Checks if a number is prime.

		:param n: The number to check.
		:return: True if the number is prime, False otherwise.
		"""
		if n <= 1:
			return False
		for i in range(2, int(math.sqrt(n)) + 1):
			if n % i == 0:
					return False
		return True

	@staticmethod
	def gcd(a: int, b: int) -> int:
		"""
		Calculates the greatest common divisor (GCD) of two numbers using the Euclidean algorithm.

		:param a: The first number.
		:param b: The second number.
		:return: The GCD of the two numbers.
		"""
		while b:
			a, b = b, a % b
		return a

	@staticmethod
	def lcm(a: int, b: int) -> int:
		"""
		Calculates the least common multiple (LCM) of two numbers.

		:param a: The first number.
		:param b: The second number.
		:return: The LCM of the two numbers.
		"""
		return abs(a * b) // MathUtils.gcd(a, b)

	@staticmethod
	def to_degrees(radians: float) -> float:
		"""
		Converts an angle from radians to degrees.

		:param radians: The angle in radians.
		:return: The angle in degrees.
		"""
		return math.degrees(radians)

	@staticmethod
	def to_radians(degrees: float) -> float:
		"""
		Converts an angle from degrees to radians.

		:param degrees: The angle in degrees.
		:return: The angle in radians.
		"""
		return math.radians(degrees)

	@staticmethod
	def sin_deg(degrees: float) -> float:
		"""
		Calculates the sine of an angle in degrees.

		:param degrees: The angle in degrees.
		:return: The sine of the angle.
		"""
		radians = MathUtils.to_radians(degrees)
		return math.sin(radians)

	@staticmethod
	def cos_deg(degrees: float) -> float:
		"""
		Calculates the cosine of an angle in degrees.

		:param degrees: The angle in degrees.
		:return: The cosine of the angle.
		"""
		radians = MathUtils.to_radians(degrees)
		return math.cos(radians)

	@staticmethod
	def tan_deg(degrees: float) -> float:
		"""
		Calculates the tangent of an angle in degrees.

		:param degrees: The angle in degrees.
		:return: The tangent of the angle.
		"""
		radians = MathUtils.to_radians(degrees)
		return math.tan(radians)

	@staticmethod
	def log(base: float, number: float) -> float:
		"""
		Calculates the logarithm of a number with a given base.

		:param base: The base of the logarithm.
		:param number: The number to calculate the logarithm of.
		:return: The logarithm of the number to the given base.
		"""
		return math.log(number, base)

	@staticmethod
	def mean(numbers: list) -> float:
		"""
		Calculates the mean (average) of a list of numbers.

		:param numbers: A list of numbers.
		:return: The mean of the numbers.
		"""
		return sum(numbers) / len(numbers) if numbers else 0

	@staticmethod
	def median(numbers: list) -> float:
		"""
		Calculates the median of a list of numbers.

		:param numbers: A list of numbers.
		:return: The median of the numbers.
		"""
		sorted_numbers = sorted(numbers)
		length = len(sorted_numbers)
		middle = length // 2
		if length % 2 == 0:
			return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2
		return sorted_numbers[middle]

	@staticmethod
	def mode(numbers: list) -> list:
		"""
		Calculates the mode(s) of a list of numbers.

		:param numbers: A list of numbers.
		:return: The mode(s) of the numbers.
		"""
		from collections import Counter
		count = Counter(numbers)
		max_count = max(count.values())
		return [num for num, freq in count.items() if freq == max_count]
