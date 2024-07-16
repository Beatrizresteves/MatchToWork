import unittest
from datetime import datetime
from models import service
from app import app
import json

class TestService(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_create_service(self):
        new_service = {
            'service_type_id' : 1,
            'client_id': 1,
            'start_date': '2024-07-01',
            'end_date': '2024-07-02',
            'status': 'Em andamento'
        }
        response = self.app.post('api/services', data=json.dumps(new_service), content_type='application/json') 
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('service_id', data)
        self.assertEqual(data['service_type_id'], 1)
        self.assertEqual(data['client_id'], 1)
        self.assertEqual(data['status'],'Em andamento')
        
if __name__ == '__main__':
    unittest.main()