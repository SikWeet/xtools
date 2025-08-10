class Find:
	@staticmethod
	def __detect_and_convert(lst: list[int | str]):
		if all(isinstance(x, int) for x in lst):
			return lst

		if all(isinstance(x, (int, str)) and str(x).isdigit() for x in lst):
			return list(map(int, lst))

		return lst

	@staticmethod
	def __all_is_type(lst: list[int | str | bool], is_type: int | str | bool) -> bool:
		response = all(isinstance(x, is_type) for x in lst)
		if not response:
			raise ValueError(f"Expected on input {is_type}")
		return True

	@staticmethod
	def __all_same_type(lst):
		types = set(map(type, lst))  # Собираем все типы в множестве
		response = types.pop() if len(types) == 1 else False
		if not response:
			raise ValueError("The list must contain a single data type")
		return response

	@staticmethod
	def __get_max_integer(numbers: list[int]) -> int:
		if Find.__all_is_type(numbers, int):
			return max(numbers)

	@staticmethod
	def __get_max_len(strings: list[str]) -> int:
		if Find.__all_is_type(strings, str):
			return max(strings, key=len)

	@staticmethod
	def get_max(*args: list[int | str]) -> int | str:
		"""Finds the largest number or the longest text depending on the content in the list. Supports nested lists.\n
		return ` int ` | ` str ` | ` list `\n
		Example #1:
		---
		```
		Find.get_max([1, 3, 6]) # return: dict(max_number=6)
		Find.get_max(['1', '3', '6']) # return: dict(max_number=6)
		Find.get_max(['hello', 'what is?', 'I using XTools']) # return: dict(max_len='I using XTools')

		```
		Example #2:
		---
		```
		Find.get_max([1, 3, 6], ['hello', 'what is?', 'I using XTools'])
		
		returned:
			type: dict
			result: dict(max_number=6, max_len='I using XTools')
		```
		"""
		result = dict()
		for arg in args:
			lst = Find.__detect_and_convert(arg)
			_type = Find.__all_same_type(lst)
			if _type is int:
				result.update(dict(max_number=Find.__get_max_integer(lst)))
			elif _type is str:
				result.update(dict(max_len=Find.__get_max_len(lst)))
		return result

	@staticmethod
	def by_key_value(data: dict, key: str, value: str | int):
		"""Search for all elements in the dictionary list where dict[key] == value"""
		results = [item for item in data if isinstance(item, dict) and item.get(key) == value]
		return results

	@staticmethod
	def contains(data: dict, key: str, substring: str):
		"""Search all elements of the dictionary list where substring is contained in dict[key] (case insensitive)"""
		substring = str(substring).lower()
		results = [
			item for item in data 
			if isinstance(item, dict) and key in item and substring in str(item[key]).lower()
		]
		return results