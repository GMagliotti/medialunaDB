class Client:
    def __init__(self, client_id, first_name, last_name, address, active, phone_list):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.active = active
        self.phone_list = phone_list

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "active": self.active,
            "phone": [phone.to_dict() for phone in self.phone_list]
        }
