from datetime import datetime
class ServiceType:
    def __init__(self, service_type_id, name,  created_at=None, updated_at=None, description=None):
        self.service_type_id = service_type_id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def from_db_row(cls, row):
        service_type_id, name, description, created_at, updated_at = row
        return cls(service_type_id, name, description, created_at, updated_at)
