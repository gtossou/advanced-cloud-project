import pytest
from fastapi.testclient import TestClient
from src.files_api.main import create_app

from tests.consts import TEST_BUCKET_NAME, REGION_NAME

# Fixture for FastAPI test client
@pytest.fixture
def client(mocked_aws) -> TestClient: 
    app = create_app(s3_bucket_name=TEST_BUCKET_NAME) # pylint: disable=unused-argument
    with TestClient(app) as client:
        yield client


# def test_upload_file(client: TestClient): 
#     ...


# def test_list_files_with_pagination(client: TestClient): 
#     ...

# def test_get_file_metadata(client: TestClient): 
#     ...

# def test_get_file(client: TestClient): 
#     ...

# def test_delete_file(client: TestClient): 
#     ...
