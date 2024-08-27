from datetime import datetime

class ServiceType:
    def __init__(self, service_type_id, name, created_at=None, updated_at=None, description=None):
        self.service_type_id = service_type_id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def from_db_row(cls, row):
        service_type_id, name, description, created_at, updated_at = row
        return cls(service_type_id, name, description, created_at, updated_at)

    def __eq__(self, other):
        if not isinstance(other, ServiceType):
            return False
        return (
            self.service_type_id == other.service_type_id and
            self.name == other.name and
            self.description == other.description and
            self.created_at == other.created_at and
            self.updated_at == other.updated_at
        )

    def __lt__(self, other):
        if not isinstance(other, ServiceType):
            return NotImplemented
        return (self.service_type_id, self.name, self.description, self.created_at, self.updated_at) < \
               (other.service_type_id, other.name, other.description, other.created_at, other.updated_at)
