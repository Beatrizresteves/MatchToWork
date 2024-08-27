import unittest
from typing import List
from models.service import Service
from repository.service_repository import ServiceRepository, IServiceRepository
from api.service_api import Endpoints

class MockServiceRepository(IServiceRepository):
    def __init__(self) -> None:
        super().__init__()
        self.services = [
            Service(1, 1, 1, "2024-01-01", "2024-01-07", "active"),
            Service(2, 2, 2, "2024-02-01", "2024-02-07", "completed"),
        ]

    def get_services(self, limit: int, offset: int) -> List[Service]:
        return self.services[offset:offset + limit]

    def get_service(self, service_id: int) -> Service:
        for s in self.services:
            if s.service_id == service_id:
                return s
        return None

    def add_service(self, service: Service) -> Service:
        self.services.append(service)
        return service

    def put_service(self, service: Service) -> Service:
        for idx, s in enumerate(self.services):
            if s.service_id == service.service_id:
                self.services[idx] = service
                return service
        return None

    def patch_service(self, service: Service) -> Service:
        for idx, s in enumerate(self.services):
            if s.service_id == service.service_id:
                if service.service_type_id is not None:
                    s.service_type_id = service.service_type_id
                if service.client_id is not None:
                    s.client_id = service.client_id
                if service.start_date is not None:
                    s.start_date = service.start_date
                if service.end_date is not None:
                    s.end_date = service.end_date
                if service.status is not None:
                    s.status = service.status
                return s
        return None

    def delete_service(self, service_id: int) -> dict:
        service_to_delete = next((s for s in self.services if s.service_id == service_id), None)
        if service_to_delete:
            self.services.remove(service_to_delete)
            return {"message": "Service deleted successfully"}
        else:
            return {"message": "Service not found"}

class TestServiceEndpoints(unittest.TestCase):
    def setUp(self):
        mock = MockServiceRepository()
        self.endpoints = Endpoints(mock)

    def test_get_services(self):
        services, status = self.endpoints.get_services()
        expected = [
            Service(1, 1, 1, "2024-01-01", "2024-01-07", "active"),
            Service(2, 2, 2, "2024-02-01", "2024-02-07", "completed"),
        ]
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(sorted(services), sorted(expected), "should return all services")

    def test_create_service(self):
        new_service = Service(3, 3, 3, "2024-03-01", "2024-03-07", "pending")
        created_service, status = self.endpoints.create_service(new_service)
        
        self.assertEqual(status, 201, "should return Created code")
        self.assertEqual(created_service, new_service, "should return the created service")
        self.assertIn(new_service, self.endpoints.repository.services, "new service should be in repository")

    def test_patch_service(self):
        service_to_update = Service(2, 2, 2, "2024-02-01", "2024-02-07", "in-progress")
        
        updated_service, status = self.endpoints.patch_service(service_to_update)
        
        self.assertEqual(status, 200, "should return OK code")
        
        self.assertEqual(updated_service.service_id, service_to_update.service_id, "should return the correct service_id")
        self.assertEqual(updated_service.service_type_id, service_to_update.service_type_id, "should return the correct service_type_id")
        self.assertEqual(updated_service.client_id, service_to_update.client_id, "should return the correct client_id")
        self.assertEqual(updated_service.start_date, service_to_update.start_date, "should return the correct start_date")
        self.assertEqual(updated_service.end_date, service_to_update.end_date, "should return the correct end_date")
        self.assertEqual(updated_service.status, service_to_update.status, "should return the correct status")
        
        self.assertIn(updated_service, self.endpoints.repository.services, "patched service should be in repository")

    def test_put_service(self):
        service = Service(2, 2, 2, "2024-02-01", "2024-02-07", "completed")
        updated_service, status = self.endpoints.put_service(service)
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(updated_service, service, "should return the replaced service")
        self.assertIn(updated_service, self.endpoints.repository.services, "replaced service should be in repository")

    def test_delete_service(self):
        service_id_to_delete = 2
        response, status = self.endpoints.delete_service(service_id_to_delete)
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(response, {"message": "Service deleted successfully"}, "should return successful deletion message")
        self.assertNotIn(service_id_to_delete, [s.service_id for s in self.endpoints.repository.services], "service should be removed from repository")

if __name__ == "__main__":
    unittest.main()
