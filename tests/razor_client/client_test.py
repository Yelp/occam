import mock
import testify as T

from occam.razor_client.client import RazorClient


class RazorClientTestCase(T.TestCase):

    @T.setup
    def create_fixtures(self):
        self.fixture_hostname = "foo"
        self.fixture_port = 8000
        self.client = RazorClient(self.fixture_hostname, self.fixture_port, lazy_discovery=True)


class RazorClientUrlBuilderTest(RazorClientTestCase):

    def test_make_netloc(self):
        expected_netloc = "%s:%s" % (self.fixture_hostname, self.fixture_port)
        actual_netloc = self.client._make_netloc()
        T.assert_equal(expected_netloc, actual_netloc)

    def test_make_razor_url(self):
        test_path = "/api/nodes"
        expected_url = "http://%s:%s%s" % (self.fixture_hostname,
            self.fixture_port,
            test_path)
        actual_url = self.client._make_razor_url(test_path)
        T.assert_equal(expected_url, actual_url)

    def test_make_razor_url_no_leading_slash(self):
        test_path = "api/nodes"
        expected_url = "http://%s:%s/%s" % (self.fixture_hostname,
            self.fixture_port,
            test_path)
        actual_url = self.client._make_razor_url(test_path)
        T.assert_equal(expected_url, actual_url)


class RazorClientGetTest(RazorClientTestCase):

    @T.setup_teardown
    def mock_requests(self):
        with mock.patch("occam.razor_client.client.requests") as self.mock_requests:
            self.mock_response = mock.Mock()
            self.mock_response.text = mock.sentinel.response_text
            self.mock_requests.get.return_value = self.mock_response

            yield

    def test_get_with_json(self):
        test_path = "/api/policies"
        expected_get_path = self.client._make_razor_url(test_path)
        self.client.get_path(test_path, response_as_json=True)

        self.mock_requests.get.assert_called_once_with(expected_get_path)
        self.mock_response.raise_for_status.assert_called_once_with()
        self.mock_response.json.assert_called_once_with()

    def test_get_without_json(self):
        test_path = "/api/policies"
        expected_get_path = self.client._make_razor_url(test_path)
        response = self.client.get_path(test_path, response_as_json=False)

        self.mock_requests.get.assert_called_once_with(expected_get_path)
        self.mock_response.raise_for_status.assert_called_once_with()
        T.assert_equal(response, self.mock_response.text)

