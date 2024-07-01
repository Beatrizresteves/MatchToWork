from datetime import datetime


class Service:
    def __init__(self, service_id, service_type_id, client_id, start_date=None, end_date=None, status=None,  created_at=None, updated_at=None):
        self.service_id = service_id
        self.service_type_id = service_type_id
        self.client_id = client_id
        self.start_date = start_date or datetime.utcnow()
        self.end_date = end_date
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def from_db_row(cls, row):
        service_id, service_type_id, client_id, start_date, end_date, created_at, updated_at, status = row, 
        return cls(service_id, service_type_id, client_id, start_date, end_date, status, created_at, updated_at)
