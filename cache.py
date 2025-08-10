import time
from collections import OrderedDict

class Cache:
	"""
	A class for caching data with the ability to set a time to live (TTL) for each item.
	"""

	def __init__(self, ttl: int = 60, max_size: int = 100):
		"""
		Initialises the cache with the specified parameters.

		:param ttl: Time to Live (TTL) for each item in the cache in seconds (default is 60 seconds).
		:param max_size: Maximum cache size (default is 100 items).
		"""
		self.__ttl = ttl
		self.__max_size = max_size
		self.__cache = OrderedDict()

	def _clear_expired(self):
		"""
		Removes obsolete items from the cache.
		"""
		current_time = time.time()
		keys_to_delete = [key for key, (value, timestamp) in self.__cache.items() if current_time - timestamp > self.__ttl]

		for key in keys_to_delete:
			del self.__cache[key]

	def _evict_if_needed(self):
		"""
		Checks if the maximum cache size has been exceeded and deletes old items if necessary.
		"""
		if len(self.__cache) > self.__max_size:
			self.__cache.popitem(last=False)

	def set(self, key: str, value: any):
		"""
		Sets the value to cache.

		:param key: Key for the cached value
		:param value: Value for caching
		"""
		self._clear_expired()  # Очищаем устаревшие данные перед записью нового значения
		self.__cache[key] = (value, time.time())  # Сохраняем данные с меткой времени
		self._evict_if_needed()  # Проверяем, нужно ли освободить место

	def get(self, key: str) -> any:
		"""
		Retrieves a value from the cache by key.

		:param key: Key to find the value
		:return: Value from cache or None if not found or out of date
		"""
		self._clear_expired()  # Очищаем устаревшие данные перед получением значения
		if key in self.__cache:
			return self.__cache[key][0]  # Возвращаем только значение (не метку времени)
		return None

	def delete(self, key: str):
		"""
		Deletes a value from the cache by key.

		:param key: Delete key
		"""
		if key in self.__cache:
			del self.__cache[key]

	def clear(self):
		"""
		Clears all cache.
		"""
		self.__cache.clear()

	def size(self) -> int:
		"""
		Returns the current number of items in the cache.
		"""
		return len(self.__cache)
