import unittest, os, sys
from flask_testing import TestCase
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), '../../'))
from server import settings as s
from server.server import app

class TestServer(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_root_route(self):
        response = self.client.get(s.ROOT_PATH)
        self.assertEquals(response.status_code, 200)

    def test_fail_to_collect_emissions_route(self):
        response = self.client.post(s.EMISSIONS_PATH, {})
        self.assertEquals(response.status_code, 400)

    def test_show_emissions_by_vehicle_id_route(self):
        response = self.client.get(s.VEHICLES_PATH + 'b962b10e-4de4-4656-9390-5ae724aef13d')
        self.assertEquals(response.status_code, 200)

    def test_show_emissions_by_vehicle_type_route(self):
        response = self.client.get(s.VEHICLES_TYPE_PATH + 'bus')
        self.assertEquals(response.status_code, 200)

    def test_show_emissions_route(self):
        response = self.client.get(s.EMISSIONS_PATH)
        self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()