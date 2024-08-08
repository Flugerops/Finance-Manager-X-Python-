import functools
import unittest
from frontend import app
from flask.testing import FlaskClient


def force_login(user_id=None):
    def inner(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if user_id:
                for key, val in kwargs.items():
                    if isinstance(val, FlaskClient):
                        with val:
                            with val.session_transaction() as sess:
                                sess['_user_id'] = user_id
                            return f(*args, **kwargs)
            return f(*args, **kwargs)

        return wrapper

    return inner

class FrontendUnitTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
            
    @force_login(user_id=0)
    def test_index(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()