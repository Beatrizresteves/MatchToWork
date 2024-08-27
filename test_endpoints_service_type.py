import unittest
from typing import List
from models.servicetype import ServiceType
from repository.service_type_repository import ServiceTypeRepository, IServiceTypeRepository
from api.service_type_api import Endpoints  # Ajuste conforme o nome correto do módulo e classe de endpoints

class MockServiceTypeRepository(IServiceTypeRepository):
    def __init__(self) -> None:
        super().__init__()
        self.service_types = [
            ServiceType(1, "Type 1", "Description 1"),
            ServiceType(2, "Type 2", "Description 2"),
        ]

    def get_service_types(self, limit: int, offset: int) -> List[ServiceType]:
        return self.service_types[offset:offset + limit]

    def get_service_type(self, service_type_id: int) -> ServiceType:
        for st in self.service_types:
            if st.service_type_id == service_type_id:
                return st
        return None

    def add_service_type(self, service_type: ServiceType) -> ServiceType:
        self.service_types.append(service_type)
        return service_type

    def put_service_type(self, service_type: ServiceType) -> ServiceType:
        for idx, st in enumerate(self.service_types):
            if st.service_type_id == service_type.service_type_id:
                self.service_types[idx] = service_type
                return service_type
        return None

    def patch_service_type(self, service_type: ServiceType) -> ServiceType:
        for idx, st in enumerate(self.service_types):
            if st.service_type_id == service_type.service_type_id:
                if service_type.name is not None:
                    st.name = service_type.name
                if service_type.description is not None:
                    st.description = service_type.description
                return st
        return None

    def delete_service_type(self, service_type_id: int) -> dict:
        service_type_to_delete = next((st for st in self.service_types if st.service_type_id == service_type_id), None)
        if service_type_to_delete:
            self.service_types.remove(service_type_to_delete)
            return {"message": "ServiceType deleted successfully"}
        else:
            return {"message": "ServiceType not found"}

class TestServiceTypeEndpoints(unittest.TestCase):
    def setUp(self):
        mock = MockServiceTypeRepository()
        self.endpoints = Endpoints(mock)

    def test_get_service_types(self):
        service_types, status = self.endpoints.get_service_types()
        expected = [
            ServiceType(1, "Type 1", "Description 1"),
            ServiceType(2, "Type 2", "Description 2"),
        ]
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(sorted(service_types), sorted(expected), "should return all service types")

    def test_get_service_type(self):
        service_type_id = 1
        service_type, status = self.endpoints.get_service_type(service_type_id)
        expected = ServiceType(1, "Type 1", "Description 1")
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(service_type, expected, "should return the correct service type")

    def test_create_service_type(self):
        new_service_type = ServiceType(None, "New Type", "New Description")
        created_service_type, status = self.endpoints.create_service_type(new_service_type)
        
        self.assertEqual(status, 201, "should return Created code")
        self.assertEqual(created_service_type.name, "New Type", "should return the created service type")
        self.assertIn(created_service_type, self.endpoints.repository.service_types, "new service type should be in repository")

    def test_put_service_type(self):
        service_type = ServiceType(2, "Updated Type", "Updated Description")
        updated_service_type, status = self.endpoints.put_service_type(service_type)
        
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(updated_service_type, service_type, "should return the updated service type")
        self.assertIn(updated_service_type, self.endpoints.repository.service_types, "updated service type should be in repository")

    def test_patch_service_type(self):
        service_type_to_update = ServiceType(2, "Patched Type", "Patched Description")
        updated_service_type, status = self.endpoints.patch_service_type(service_type_to_update)
        
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(updated_service_type.name, service_type_to_update.name, "should return the correct name")
        self.assertEqual(updated_service_type.description, service_type_to_update.description, "should return the correct description")
        self.assertIn(updated_service_type, self.endpoints.repository.service_types, "patched service type should be in repository")

    def test_delete_service_type(self):
        service_type_id_to_delete = 2
        response, status = self.endpoints.delete_service_type(service_type_id_to_delete)
        
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(response, {"message": "ServiceType deleted successfully"}, "should return successful deletion message")
        self.assertNotIn(service_type_id_to_delete, [st.service_type_id for st in self.endpoints.repository.service_types], "service type should be removed from repository")

if __name__ == "__main__":
    unittest.main()
