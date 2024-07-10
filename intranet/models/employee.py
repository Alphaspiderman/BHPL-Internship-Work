class Employee:
    fields = [
        "Employee_Id",
        "First_Name",
        "Last_Name",
        "Email",
        "Emp_Type",
        "Department",
        "Store_Code",
        "Grade",
    ]

    hidden_fields = []

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

    def get_schema(self) -> dict:
        schema = self.fields.copy()
        for field in self.hidden_fields:
            schema.remove(field)
        return schema

    def get_full_name(self) -> str:
        return f"{self.First_Name} {self.Last_Name}"
