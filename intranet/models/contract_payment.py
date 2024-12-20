class ContractPayment:
    fields = [
        "Contract_Id",
        "Vendor_Code",
        "Department_Code",
        "Invoice_Status",
        "Due_Date",
        "Due_Amount",
        "Payment_Date",
        "Payment_Amount",
        "Invoice_Frequency",
    ]

    convert_fields = {
        "Due_Date": lambda x: x.strftime("%Y-%m-%d") if x else None,
        "Due_Amount": lambda x: str(x) if x else None,
        "Payment_Date": lambda x: x.strftime("%Y-%m-%d") if x else None,
        "Payment_Amount": lambda x: str(x) if x else None,
    }

    hidden_fields = ["Contract_Id"]

    def __init__(self, data):
        for idx, field in enumerate(self.fields):
            setattr(self, field, data[idx])

    def to_dict(self) -> dict:
        return {field: getattr(self, field) for field in self.fields}

    def get_data(self) -> dict:
        data = self.to_dict()
        for field in self.hidden_fields:
            data.pop(field, None)
        for field, convert in self.convert_fields.items():
            data[field] = convert(data[field])
        return data

    @classmethod
    def get_schema(self) -> list:
        fields = self.fields.copy()
        for field in self.hidden_fields:
            fields.remove(field)
        return fields
