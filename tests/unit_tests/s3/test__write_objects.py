import boto3
from files_api.s3.write_objects import upload_s3_object
import os


from moto import mock_aws

from tests.consts import TEST_BUCKET_NAME, REGION_NAME

@mock_aws
def test__upload_s3_object(mocked_aws):

    object_key = "test.txt"
    file_content = b"Hello, World!"
    content_type = "text/plain"
    object_key = "test.txt"


    # Upload the object this a particular content type
    upload_s3_object(bucket_name=TEST_BUCKET_NAME, object_key=object_key, file_content=file_content,content_type=content_type)
    
    # Check the file is uploaded with the right content type
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=object_key)
    assert response["Body"].read() == b"Hello, World!"
    assert response["ContentType"] == content_type



