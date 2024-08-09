import functools
import unittest
from flask import url_for
from flask_login import current_user, login_user
from flask_testing import TestCase
from datetime import datetime
from frontend import app
from frontend.db import Base, engine, Session, User


class BaseTestCase(TestCase):
    
    def create_app(self):
        return app

    def setUp(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        user = User(nickname="admin", password=1234)
        self.session.add(user)
        self.session.commit()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)


class FrontendUnitTest(BaseTestCase):

    def test_login(self):
        with self.client:
            response = self.client.post(
                "/login", data=dict(nickname="admin", password=1234))
            self.assert200(response)

    def test_index(self):
        with self.client:
            login_user(self.session.query(User).where(User.nickname == "admin").first())
            print(current_user.nickname)
            index = self.client.get("/")
            self.assert200(index)

    def test_clear_filters(self):
        with self.client:
            login_user(self.session.query(User).where(User.nickname == "admin").first())
            filters = self.client.post("/", data={"action": "apply", "start-date": datetime.now().isoformat()})
            self.assert200(filters)
    
    def test_charts(self):
        with self.client:
            login_user(self.session.query(User).where(User.nickname == "admin").first())
            charts = self.client.get("/charts")
            self.assert200(charts)
    
    def test_registration(self):
        with self.client:
            registration = self.client.post("/register", data={"nickname": "register", "password": 1234})
            self.assert200(registration)
            
            
if __name__ == "__main__":
    unittest.main()
