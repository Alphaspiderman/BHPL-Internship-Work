from json import loads


class VendorContract:
    fields = [
        "Contract_Id",
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
        "Contract_Active": lambda x: "Yes" if x else "No",
        "AMC_Start_Date": lambda x: x.strftime("%Y-%m-%d"),
        "AMC_End_Date": lambda x: x.strftime("%Y-%m-%d"),
        "Next_Reminder": lambda x: x.strftime("%Y-%m-%d") if x else "Pending Setup",
        "Invoice_Base_Cost": lambda x: str(x) if x else None,
        "Reminder_Addresses": lambda x: ", ".join(loads(x)) if x else None,
    }

    hidden_fields = ["Contract_Id", "Contract_Description"]

    def __init__(self, data):
        for idx, field in enumerate(self.fields):
            setattr(self, field, data[idx])

    def to_dict(self) -> dict:
        return {field: getattr(self, field) for field in self.fields}

    def get_data(self, show_all: bool = False) -> dict:
        data = self.to_dict()
        hidden_fields = self.hidden_fields.copy()
        if not show_all:
            for field in hidden_fields:
                data.pop(field, None)
        for field, convert in self.convert_fields.items():
            data[field] = convert(data[field])
        return data

    def get_schema(self, show_all: bool = False) -> list:
        schema = self.fields.copy()
        hidden_fields = self.hidden_fields.copy()
        if not show_all:
            for field in hidden_fields:
                schema.remove(field)
        return schema
