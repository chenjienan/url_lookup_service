import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Url


class TestUrlService(BaseTestCase):
    """Tests for the URL Lookup Service."""
    def test_urls(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_url(self):
        """Ensure a new url can be added to the database."""
        with self.client:
            response = self.client.post(
                '/urls',
                data=json.dumps({
                    'url': 'https://www.google.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('https://www.google.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_url_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/urls',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_duplicate_url(self):
        """Ensure error is thrown if the url already exists."""
        with self.client:
            self.client.post(
                '/urls',
                data=json.dumps({
                    'url': 'https://www.amazon.com'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/urls',
                data=json.dumps({
                    'url': 'https://www.amazon.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('That url already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_urlinfo_url_not_exist(self):
        """Ensure get URL info behaves correctly."""
        with self.client:
            response = self.client.get(f'/urlinfo/google.com:443/something.html%3Fq%3Dgo%2Blang')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('false', data['isMalware'])

    def test_get_urlinfo_url_exists(self):
        """Ensure get URL info behaves correctly when url is empty."""
        url = Url(url='abc.com')
        db.session.add(url)
        db.session.commit()

        with self.client:
            response = self.client.get(f'/urlinfo/abc.com')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('true', data['isMalware'])

    def test_get_urlinfo_url_empty(self):
        with self.client:
            response = self.client.get(f'/urlinfo/')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
