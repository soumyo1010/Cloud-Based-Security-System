import boto3
import botocore
import os

# Initialize the S3 client
s3 = boto3.client('s3', region_name='eu-north-1')  # Replace 'eu-north-1' with your region
bucket_name = 'mysm10'  # Replace with your S3 bucket name

class ProgressPercentage:
    def __init__(self, file_path):
        self._file_path = file_path
        self._size = float(os.path.getsize(file_path))
        self._seen_so_far = 0

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        percentage = (self._seen_so_far / self._size) * 100
        print(f"\rUploading {self._file_path}: {percentage:.2f}%", end="")

def upload_to_s3(file_path, key):
    """
    Uploads a file to the specified S3 bucket.
    
    :param file_path: Path to the local file to upload.
    :param key: S3 object key (path in the bucket).
    """
    try:
        s3.upload_file(
            file_path,
            bucket_name,
            key,
            Callback=ProgressPercentage(file_path))
        print(f"\nFile uploaded successfully to s3://{bucket_name}/{key}")
    except botocore.exceptions.NoCredentialsError:
        print("Error: AWS credentials not found.")
    except botocore.exceptions.PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
    except botocore.exceptions.EndpointConnectionError:
        print("Error: Could not connect to AWS S3.")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Example usage with full file path (using raw string)
upload_to_s3(r"C:\Users\SOUMYO\Downloads\local_video.mp4", 'videos/local_video.mp4')