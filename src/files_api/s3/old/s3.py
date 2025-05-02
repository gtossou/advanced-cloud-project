import boto3

BUCKET_NAME = "advanced-cloud-prj-s3"
PROFILE_NAME = "course-project"

session = boto3.Session(profile_name=PROFILE_NAME)
s3_client = session.client("s3", region_name="eu-west-1")

s3_client.put_object(Bucket=BUCKET_NAME, Key="folder/test.txt", Body="Hello, World!", ContentType="text/plain")
