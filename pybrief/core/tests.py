from django.test import TestCase, Client


class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_success(self):
        """Home page have to returns status code 200 in any case"""

        self.assertEqual(self.client.get('/').status_code, 200)
