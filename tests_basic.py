# tests/test_basic.py

import unittest
from flaskblog import create_app

app = create_app()


class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get("/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email", response.data)
        self.assertIn(b"Password", response.data)
        self.assertIn(b"Log In", response.data)

    # Ensure that register page loads
    def test_register_route_works_as_expected(self):
        tester = app.test_client(self)
        response = tester.get("/register", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username", response.data)
        self.assertIn(b"Email", response.data)
        self.assertIn(b"Password", response.data)
        self.assertIn(b"Confirm Password", response.data)


if __name__ == "__main__":
    unittest.main()

