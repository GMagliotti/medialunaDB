class InvoiceDetail:
    def __init__(self, item_pos: int, item_qty: float, product_id: int):
        self.item_pos = item_pos
        self.item_qty = item_qty
        self.product_id = product_id