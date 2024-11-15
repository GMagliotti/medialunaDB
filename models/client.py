from phone import Phone

class Client:
    def __init__(self, client_id: int, first_name: str, last_name: str, address: str, active: int, phone: Phone):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.active = active
        self.phone: Phone = phone