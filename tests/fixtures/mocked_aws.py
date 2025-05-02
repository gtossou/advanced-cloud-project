from pytest import fixture
import os
from tests.consts import REGION_NAME, TEST_BUCKET_NAME
import boto3
from moto import mock_aws

def point_away_from_aws():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = REGION_NAME

@fixture
def mocked_aws():
    with mock_aws():
        point_away_from_aws()
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME,CreateBucketConfiguration={"LocationConstraint": REGION_NAME})
        
        yield
        #Get the objects in the bucket and delete it with its contents
        response = s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
        for obj in response.get("Contents", []):
            s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])

        s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)