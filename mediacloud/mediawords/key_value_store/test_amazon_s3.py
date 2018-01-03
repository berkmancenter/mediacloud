import pytest

from mediawords.key_value_store.amazon_s3 import AmazonS3Store
from mediawords.key_value_store.test_amazon_s3_credentials import (
    TestAmazonS3CredentialsTestCase, get_test_s3_credentials)


test_credentials = get_test_s3_credentials()

pytest_amazon_s3_credentials_set = pytest.mark.skipif(
    test_credentials is None,
    reason="Amazon S3 test credentials are not set in environment / configuration"
)


@pytest_amazon_s3_credentials_set
class TestAmazonS3StoreTestCase(TestAmazonS3CredentialsTestCase):
    def _initialize_store(self) -> AmazonS3Store:
        return AmazonS3Store(access_key_id=test_credentials['access_key_id'],
                             secret_access_key=test_credentials['secret_access_key'],
                             bucket_name=test_credentials['bucket_name'],
                             directory_name=test_credentials['directory_name'])

    def _expected_path_prefix(self) -> str:
        return 's3:'

    def test_key_value_store(self):
        self._test_key_value_store()
