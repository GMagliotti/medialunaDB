class Phone:
    def __init__(self, area_code, phone_number, _type, client_id):
        self.area_code = area_code
        self.phone_number = phone_number
        self._type = _type
        self.client_id = client_id

    def to_dict(self):
        return {
            "area_code": self.area_code,
            "phone_number": self.phone_number,
            "_type": self._type,
            "client_id": self.client_id
        }
