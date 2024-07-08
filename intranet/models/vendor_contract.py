class VendorContract:
    fields = [
        "Vendor_Code",
        "Department_Code",
        "Contract_Active",
        "Contract_Description",
        "AMC_Start_Date",
        "AMC_End_Date",
        "File_Name",
        "Invoice_Frequency",
        "Invoice_Base_Cost",
        "Reminder_Addresses",
        "Next_Reminder",
    ]

    convert_fields = {
        "AMC_Start_Date": lambda x: x.strftime("%Y-%m-%d"),
        "AMC_End_Date": lambda x: x.strftime("%Y-%m-%d"),
        "File_Name": lambda x: f"<a href='{x}'>Click Me</a>" if x else None,
        "Next_Reminder": lambda x: x.strftime("%Y-%m-%d") if x else None,
    }

    hidden_fields = ["Contract_Description"]

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

    def get_schema(self) -> list:
        schema = self.fields.copy()
        for field in self.hidden_fields:
            schema.remove(field)
        return schema
