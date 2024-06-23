class ServiceType:
    def __init__(self, service_type_id, name, description=None):
        self.service_type_id = service_type_id
        self.name = name
        self.description = description

    @classmethod
    def from_db_row(cls, row):
        service_type_id, name, description = row
        return cls(service_type_id, name, description)
