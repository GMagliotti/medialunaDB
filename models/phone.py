class Phone:
    def __init__(self, area_code, phone_number, type, client_id):
        self.area_code = area_code
        self.phone_number = phone_number
        self.type = type
        self.client_id = client_id

    def to_dict(self):
        return {
            "area_code": self.area_code,
            "phone_number": self.phone_number,
            "type": self.type,
            "client_id": self.client_id
        }
