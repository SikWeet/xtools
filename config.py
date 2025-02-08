import configparser
import json
import os
import yaml


class Config:
	def __init__(self, filepath: str = "configure.json", autosave: bool = True):
		"""
		Convenient configuration parser

		:param __filepath: File Path. Supports ` .json `, ` .yaml `, ` .ini `
		:return: Config (self)
		"""
		self.__filepath = filepath
		self.__autosave = autosave
		self.__extension = os.path.splitext(filepath)[-1].lower()

		if not os.path.exists(filepath):
			self._create_empty_file()

		self.__data = self._load_config()
	

	def _create_empty_file(self):
		# В зависимости от формата создаём пустой конфигурационный файл
		if self.__extension == ".json":
			default_data = {}
			with open(self.__filepath, "w") as f:
					json.dump(default_data, f, indent=4)
		elif self.__extension == ".yaml" or self.__extension == ".yml":
			default_data = {}
			with open(self.__filepath, "w") as f:
					yaml.safe_dump(default_data, f)
		elif self.__extension == ".ini":
			config = configparser.ConfigParser()
			config.write(open(self.__filepath, "w"))
		else:
			raise ValueError("Unsupported file format")

	def _load_config(self):
		if self.__extension == ".json":
			with open(self.__filepath) as fp:
				return json.load(fp)
		elif self.__extension in [".yml", ".yaml"]:
			with open(self.__filepath) as fp:
				return yaml.safe_load(fp)
		elif self.__extension == ".ini":
			config = configparser.ConfigParser()
			config.read(self.__filepath)
			return {section: dict(config.items) for section in config.sections()}
		else:
			raise ValueError("Unsupported file format. Use: .json, .yaml, .ini")

	def save(self):
		if self.__extension == ".json":
			with open(self.__filepath, "w") as f:
					json.dump(self.__data, f, indent=4)
		elif self.__extension == ".yaml" or self.__extension == ".yml":
			with open(self.__filepath, "w") as f:
					yaml.safe_dump(self.__data, f)
		elif self.__extension == ".ini":
			config = configparser.ConfigParser()
			for section, values in self.__data.items():
					config[section] = values
			with open(self.__filepath, "w") as f:
					config.write(f)

	def get(self, key, default=None):
		keys = key.split(".")
		result = self.__data
		for k in keys:
			result = result.get(k, default)
			if result is default:
					break
		return result

	def set(self, key, value):
		keys = key.split(".")
		data = self.__data
		for k in keys[:-1]:
			data = data.setdefault(k, {})
		data[keys[-1]] = value
		if self.__autosave:
			self.save()
