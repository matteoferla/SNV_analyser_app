import unittest

from pyramid import testing

import transaction

from .views.default import my_view
from .models import User


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestMyViewSuccessCondition, self).setUp()
        self.init_database()
        admin = User(name='admin', role='admin')
        admin.set_password('admin')
        self.session.add(admin)

    def test_passing_view(self):
        request = dummy_request(self.session)
        basic = User(name='Bob', role='builder')
        basic.set_password('fixit')
        self.session.add(basic)
        request.user = basic
        info = my_view(request)
        self.assertEqual(info['user'].name, 'Bob')
        self.assertEqual(info['project'], 'Venus')


class TestMyViewFailureCondition(BaseTest):

    def test_failing_view(self):
        request = dummy_request(self.session)
        request.user = None
        info = my_view(request)
        self.assertEqual(info.status_int, 500)
