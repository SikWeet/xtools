import os
import json
import tempfile
import threading
import configparser
from typing import Any, Dict, Optional
from copy import deepcopy

try:
	import yaml  # PyYAML, optional dependency
except Exception:
	yaml = None

class Config:
	"""
		A utility class for loading, saving, and managing configuration files in multiple formats.

		Features:
		- Automatic detection of file format from file extension.
		- Thread-safe read/write operations with recursive merging.
		- Dot-notation key access (e.g., "database.host").
		- Automatic defaults merge.
		- Environment variable overrides (optional).
		- Safe atomic writes to prevent data corruption.

		Supported formats:
		- JSON
		- YAML
		- INI
		
		This class provides a unified interface for reading and writing configuration files,
		making it easier to work with different formats without having to write format-specific code.
	"""

	def __init__(
		self,
		path: str,
		defaults: Optional[Dict[str, Any]] = None,
		env_prefix: Optional[str] = None,
		encoding: str = "utf-8",
		create: bool = False,
	):
		"""
		Initialize the Config object.

		Args:
			path (str):
					Path to the configuration file.
			defaults (dict, optional):
					Default configuration values. Missing keys in the loaded file will
					be filled with these defaults.
			env_prefix (str, optional):
					If provided, environment variables starting with this prefix will
					override loaded configuration values.
			encoding (str):
					File encoding. Default is "utf-8".
			create (bool):
					If True and the file does not exist, create it using defaults.

		Behavior:
			- Detects file format based on extension (.json, .yaml/.yml, .ini).
			- If create=True and file doesn't exist, saves defaults immediately.
			- Otherwise, attempts to load the existing file.
		"""
		self.path = path
		self.encoding = encoding
		self.defaults = deepcopy(defaults or {})
		self.env_prefix = env_prefix
		self._lock = threading.RLock()
		self._data: Dict[str, Any] = {}
		if create and not os.path.exists(path):
			self._data = deepcopy(self.defaults)
			self.save()
		else:
			self.load()

	def _detect_format(self) -> str:
		"""
		Detect configuration file format based on file extension.

		Returns:
			str: One of "json", "yaml", or "ini".
		"""
		ext = os.path.splitext(self.path)[1].lower()
		if ext in (".yml", ".yaml"):
			return "yaml"
		if ext == ".ini":
			return "ini"
		return "json"

	def load(self) -> None:
		"""
		Load configuration from disk into memory.

		Behavior:
			- If file does not exist, loads defaults.
			- Automatically detects file format.
			- Merges defaults and applies environment variable overrides.

		Raises:
			RuntimeError: If YAML file is requested but PyYAML is not installed.
		"""
		with self._lock:
			if not os.path.exists(self.path):
					self._data = deepcopy(self.defaults)
					if self.env_prefix:
						self.update_from_env(self.env_prefix)
					return

			fmt = self._detect_format()
			with open(self.path, "r", encoding=self.encoding) as f:
					if fmt == "json":
						self._data = json.load(f) or {}
					elif fmt == "yaml":
						if yaml is None:
							raise RuntimeError("PyYAML is required to load YAML files.")
						self._data = yaml.safe_load(f) or {}
					else:  # ini
						cp = configparser.ConfigParser()
						cp.read_file(f)
						data: Dict[str, Any] = {}
						for section in cp.sections():
							data[section] = dict(cp[section])
						self._data = data

			self._merge_defaults()
			if self.env_prefix:
					self.update_from_env(self.env_prefix)

	def save(self) -> bool:
		"""
		Save configuration to disk atomically.

		Returns:
			bool: True if save was successful, otherwise raises an exception.

		Behavior:
			- Writes to a temporary file first, then replaces the original file.
			- Prevents corruption if process is interrupted mid-save.

		Raises:
			RuntimeError: If saving YAML but PyYAML is not installed.
		"""
		with self._lock:
			fmt = self._detect_format()
			# записываем в temp и затем заменяем
			tmp = tempfile.NamedTemporaryFile("w", delete=False, encoding=self.encoding)
			tmp_name = tmp.name
			try:
					if fmt == "json":
						json.dump(self._data, tmp, ensure_ascii=False, indent=2)
					elif fmt == "yaml":
						if yaml is None:
							raise RuntimeError("PyYAML is required to save YAML files.")
						yaml.safe_dump(self._data, tmp, allow_unicode=True)
					else:
						cp = configparser.ConfigParser()
						# INI не поддерживает глубокие структуры — ожидаем dict[str, dict]
						for section, vals in self._data.items():
							cp[section] = {k: str(v) for k, v in (vals or {}).items()}
						cp.write(tmp)
					tmp.flush()
					tmp.close()
					os.replace(tmp_name, self.path)
					return True
			except Exception:
					try:
						os.unlink(tmp_name)
					except Exception:
						pass
					raise

	# --- helpers: dot access, merge, env parsing ---

	def get(self, key: str, default: Any = None) -> Any:
		"""
		Retrieve a configuration value using dot notation.

		Args:
			key (str):
					Dot-separated path to the value (e.g., "database.host").
			default (Any):
					Value to return if key is missing.

		Returns:
			Any: The found value, or the provided default.
		"""
		with self._lock:
			cur = self._data
			for part in key.split("."):
					if isinstance(cur, dict) and part in cur:
						cur = cur[part]
					else:
						return default
			return deepcopy(cur)

	def set(self, key: str, value: Any) -> None:
		"""
		Set a configuration value using dot notation.

		Args:
			key (str):
					Dot-separated path (e.g., "database.host").
			value (Any):
					Value to assign.
		"""
		with self._lock:
			parts = key.split(".")
			cur = self._data
			for p in parts[:-1]:
					if p not in cur or not isinstance(cur[p], dict):
						cur[p] = {}
					cur = cur[p]
			cur[parts[-1]] = value

	def delete(self, key: str) -> bool:
		"""
		Delete a configuration key using dot notation.

		Args:
			key (str): Dot-separated path to the key.

		Returns:
			bool: True if the key was deleted, False otherwise.
		"""
		with self._lock:
			parts = key.split(".")
			cur = self._data
			for p in parts[:-1]:
					if p not in cur or not isinstance(cur[p], dict):
						return False
					cur = cur[p]
			return cur.pop(parts[-1], None) is not None

	def has(self, key: str) -> bool:
		"""
		Check if a key exists in the configuration.

		Args:
			key (str): Dot-separated path.

		Returns:
			bool: True if the key exists, False otherwise.
		"""
		return self.get(key, None) is not None

	def as_dict(self) -> Dict[str, Any]:
		"""
		Get a deep copy of the current configuration data.

		Returns:
			dict: Configuration as a dictionary.
		"""
		with self._lock:
			return deepcopy(self._data)

	def merge(self, other: Dict[str, Any]) -> None:
		"""
		Recursively merge another dictionary into the configuration.

		Args:
				other (dict):
					Dictionary whose values will overwrite existing ones.

		Behavior:
				- Nested dictionaries are merged recursively.
				- Existing keys are replaced with `other`'s values.
		"""
		def _merge(dst, src):
			for k, v in src.items():
					if k in dst and isinstance(dst[k], dict) and isinstance(v, dict):
						_merge(dst[k], v)
					else:
						dst[k] = deepcopy(v)
		with self._lock:
			_merge(self._data, other)

	def _merge_defaults(self) -> None:
		"""
		Merge default values into the current configuration.

		Behavior:
			- Missing keys in `_data` are filled from `self.defaults`.
			- Nested dictionaries are merged recursively.
		"""
		def _merge(dst, src):
			for k, v in src.items():
					if k in dst and isinstance(dst[k], dict) and isinstance(v, dict):
						_merge(dst[k], v)
					else:
						dst.setdefault(k, deepcopy(v))
		_merge(self._data, self.defaults)

	@staticmethod
	def _parse_env_value(val: str) -> Any:
		"""
		Attempt to parse an environment variable value into its native type.

		Parsing order:
			1. Boolean ("true"/"false")
			2. Integer
			3. Float
			4. JSON
			5. String (fallback)

		Args:
			val (str): Raw string value.

		Returns:
			Any: Parsed value.
		"""
		lowered = val.lower()
		if lowered in ("true", "false"):
			return lowered == "true"
		try:
			return int(val)
		except Exception:
			pass
		try:
			return float(val)
		except Exception:
			pass
		try:
			return json.loads(val)
		except Exception:
			pass
		return val

	def __enter__(self):
		"""
		Context manager entry.

		Returns:
			Config: Self instance, so usage can be:
					with Config(...) as cfg:
						cfg.set("key", "value")
		"""
		return self

	def __exit__(self, exc_type, exc, tb):
		"""
		Context manager exit. Attempts to save on exit.

		Behavior:
			- Saves current config to file when leaving context.
			- Silently ignores save errors.
		"""
		try:
			self.save()
		except Exception:
			pass
