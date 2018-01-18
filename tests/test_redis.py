from .helper import FlaskTestBase


class TestRedis(FlaskTestBase):

    def setUp(self):
        FlaskTestBase.setUp(self)
        from tigereye.extensions import redi
        self.redi = redi

    def test_redi_api(self):
        self.assertTrue(self.redi.set('foo', 'bar'))
        self.assertEqual(self.redi.get('foo').decode('utf-8'), 'bar')
        self.assertEqual(self.redi.delete('foo'), 1)
        self.assertEqual(self.redi.delete('foo'), 0)
