import boto3
import botocore
import os

# Initialize the S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_AWS_ACCESS_KEY',  # Replace with your AWS Access Key
    aws_secret_access_key='YOUR_AWS_SECRET_KEY',  # Replace with your AWS Secret Key
    region_name='eu-north-1'  # Replace with your AWS region (e.g., 'eu-north-1')
)

# Replace with your S3 bucket name
bucket_name = 'mysm10'

class ProgressPercentage:
    def __init__(self, file_path):
        self._file_path = file_path
        self._size = float(os.path.getsize(file_path))
        self._seen_so_far = 0

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        percentage = (self._seen_so_far / self._size) * 100
        print(f"\rDownloading {self._file_path}: {percentage:.2f}%", end="")

def download_from_s3(key, download_path):
    """
    Downloads a file from the specified S3 bucket.
    
    :param key: S3 object key (path in the bucket).
    :param download_path: Path to save the downloaded file locally.
    """
    try:
        s3.download_file(
            bucket_name,
            key,
            download_path,
            Callback=ProgressPercentage(download_path))
        print(f"\nFile downloaded successfully to {download_path}")
    except botocore.exceptions.NoCredentialsError:
        print("Error: AWS credentials not found.")
    except botocore.exceptions.PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
    except botocore.exceptions.EndpointConnectionError:
        print("Error: Could not connect to AWS S3.")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Example usage
download_from_s3('videos/local_video.mp4', 'downloaded_video.mp4')