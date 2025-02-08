from cryptography.fernet import Fernet

class EncryptionUtils:
	"""
	Utility class for data encryption and decryption.
	"""

	@staticmethod
	def generate_key() -> bytes:
		"""
		Generates a new encryption key.

		:return: The generated key.
		"""
		return Fernet.generate_key()

	@staticmethod
	def encrypt(data: str, key: bytes) -> str:
		"""
		Encrypts the given data using the provided key.

		:param data: The data to encrypt.
		:param key: The encryption key.
		:return: The encrypted data as a string.
		"""
		cipher = Fernet(key)
		encrypted_data = cipher.encrypt(data.encode('utf-8'))
		return encrypted_data.decode('utf-8')

	@staticmethod
	def decrypt(data: str, key: bytes) -> str:
		"""
		Decrypts the given data using the provided key.

		:param data: The data to decrypt.
		:param key: The decryption key.
		:return: The decrypted data as a string.
		"""
		cipher = Fernet(key)
		decrypted_data = cipher.decrypt(data.encode('utf-8'))
		return decrypted_data.decode('utf-8')
