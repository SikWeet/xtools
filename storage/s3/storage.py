import boto3
import aioboto3
from botocore.exceptions import BotoCoreError, ClientError


class AsyncS3Storage:
	"""
	Asynchronous class for interacting with AWS S3 or S3-compatible storage.
	"""

	def __init__(self, bucket_name: str, aws_access_key: str, aws_secret_key: str, region: str = "us-east-1"):
		self.bucket_name = bucket_name
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key
		self.region = region

	async def upload_file(self, file_path: str, s3_key: str) -> bool:
		"""Uploads a file to S3 asynchronously."""
		try:
			async with aioboto3.client(
					"s3",
					aws_access_key_id=self.aws_access_key,
					aws_secret_access_key=self.aws_secret_key,
					region_name=self.region
			) as s3:
					await s3.upload_file(file_path, self.bucket_name, s3_key)
			return True
		except (BotoCoreError, ClientError) as e:
			print(f"[AsyncS3Storage] Upload error: {e}")
			return False

	async def download_file(self, s3_key: str, file_path: str) -> bool:
		"""Downloads a file from S3 asynchronously."""
		try:
			async with aioboto3.client(
					"s3",
					aws_access_key_id=self.aws_access_key,
					aws_secret_access_key=self.aws_secret_key,
					region_name=self.region
			) as s3:
					await s3.download_file(self.bucket_name, s3_key, file_path)
			return True
		except (BotoCoreError, ClientError) as e:
			print(f"[AsyncS3Storage] Download error: {e}")
			return False

	async def delete_file(self, s3_key: str) -> bool:
		"""Deletes a file from S3 asynchronously."""
		try:
			async with aioboto3.client(
					"s3",
					aws_access_key_id=self.aws_access_key,
					aws_secret_access_key=self.aws_secret_key,
					region_name=self.region
			) as s3:
					await s3.delete_object(Bucket=self.bucket_name, Key=s3_key)
			return True
		except (BotoCoreError, ClientError) as e:
			print(f"[AsyncS3Storage] Delete error: {e}")
			return False

	async def list_files(self) -> list:
		"""Lists all files in the bucket asynchronously."""
		try:
			async with aioboto3.client(
					"s3",
					aws_access_key_id=self.aws_access_key,
					aws_secret_access_key=self.aws_secret_key,
					region_name=self.region
			) as s3:
					response = await s3.list_objects_v2(Bucket=self.bucket_name)
					return [item["Key"] for item in response.get("Contents", [])]
		except (BotoCoreError, ClientError) as e:
			print(f"[AsyncS3Storage] List error: {e}")
			return []

class S3Storage:
	"""
	Synchronous class for interacting with AWS S3 or S3-compatible storage.
	"""

	def __init__(self, bucket_name: str, aws_access_key: str, aws_secret_key: str, region: str = "us-east-1"):
		self.s3 = boto3.client(
			"s3",
			aws_access_key_id=aws_access_key,
			aws_secret_access_key=aws_secret_key,
			region_name=region
		)
		self.bucket_name = bucket_name

	def upload_file(self, file_path: str, s3_key: str) -> bool:
		"""Uploads a file to S3."""
		try:
			self.s3.upload_file(file_path, self.bucket_name, s3_key)
			return True
		except (BotoCoreError, ClientError) as e:
			print(f"[S3Storage] Upload error: {e}")
			return False

	def download_file(self, s3_key: str, file_path: str) -> bool:
		"""Downloads a file from S3."""
		try:
			self.s3.download_file(self.bucket_name, s3_key, file_path)
			return True
		except (BotoCoreError, ClientError) as e:
			print(f"[S3Storage] Download error: {e}")
			return False

	def delete_file(self, s3_key: str) -> bool:
		"""Deletes a file from S3."""
		try:
			self.s3.delete_object(Bucket=self.bucket_name, Key=s3_key)
			return True
		except (BotoCoreError, ClientError) as e:
			print(f"[S3Storage] Delete error: {e}")
			return False

	def list_files(self) -> list:
		"""Lists all files in the bucket."""
		try:
			response = self.s3.list_objects_v2(Bucket=self.bucket_name)
			return [item["Key"] for item in response.get("Contents", [])]
		except (BotoCoreError, ClientError) as e:
			print(f"[S3Storage] List error: {e}")
			return []