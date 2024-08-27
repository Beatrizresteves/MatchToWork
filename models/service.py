from datetime import datetime, timezone

class Service:
    def __init__(self, service_id, service_type_id, client_id, start_date=None, end_date=None, status=None, created_at=None, updated_at=None):
        self.service_id = service_id
        self.service_type_id = service_type_id
        self.client_id = client_id
        self.start_date = start_date or datetime.now(timezone.utc)
        self.end_date = end_date
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    @classmethod
    def from_db_row(cls, row):
        service_id, service_type_id, client_id, start_date, end_date, created_at, updated_at, status = row
        return cls(service_id, service_type_id, client_id, start_date, end_date, status, created_at, updated_at)

    def __eq__(self, other):
        if isinstance(other, Service):
            return (
                self.service_id == other.service_id and
                self.service_type_id == other.service_type_id and
                self.client_id == other.client_id and
                self.start_date == other.start_date and
                self.end_date == other.end_date and
                self.status == other.status and
                self.created_at == other.created_at and
                self.updated_at == other.updated_at
            )
        return False

    def __lt__(self, other):
        if isinstance(other, Service):
            return self.service_id < other.service_id
        return NotImplemented

    def __repr__(self):
        return (f"Service({self.service_id}, {self.service_type_id}, {self.client_id}, "
                f"{self.start_date}, {self.end_date}, {self.status}, "
                f"{self.created_at}, {self.updated_at})")
