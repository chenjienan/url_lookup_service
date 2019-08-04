import unittest

from project import db
from project.api.models import Url
from project.tests.base import BaseTestCase
from project.tests.utils import add_url

from sqlalchemy.exc import IntegrityError


class TestUrlModel(BaseTestCase):

    def test_add_url(self):
        # Arrange/Action
        cur_url = add_url('abc.com')
        # Assert
        self.assertTrue(cur_url.id)
        self.assertEqual(cur_url.url, 'abc.com')
        self.assertTrue(cur_url.active)

    def test_add_duplicate_url(self):
        # Arrange
        add_url('xyz.ca')
        duplicate_url = Url('xyz.ca')
        # Action
        db.session.add(duplicate_url)
        # Assert
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        # Arrange/Action
        cur_url = add_url('xyz.org')        
        # Assert
        self.assertTrue(isinstance(cur_url.to_json(), dict))


if __name__ == '__main__':
    unittest.main()
