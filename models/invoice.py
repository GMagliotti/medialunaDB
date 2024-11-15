from invoice_detail import InvoiceDetail

class Invoice:
    def __init__(self, invoice_id: int, date, amount_before_tax: float, tax: float, client_id: int, invoice_detail: InvoiceDetail):
        self.invoice_id = invoice_id
        self.date = date
        self.amount_before_tax = amount_before_tax
        self.tax = tax
        self.client_id = client_id
        self.invoice_detail: InvoiceDetail = invoice_detail
