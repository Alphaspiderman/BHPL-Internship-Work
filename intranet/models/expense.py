class Expense:
    fields = [
        "Id",
        "Employee_Id",
        "Date_Of_Expense",
        "Location",
        "Stationary",
        "Welfare_Meal",
        "Promotion_Meal",
        "Hotel_Rent",
        "Connectivity_Charges",
        "Travel_Charge",
        "Others",
        "Bill_Attached",
        "Personal_Vehicle_Dist",
        "Reason",
    ]

    hidden_fields = ["Id"]

    convert_fields = {
        "Date_Of_Expense": lambda x: x.strftime("%Y-%m-%d"),
        "Receipt_Attached": lambda x: "Yes" if x else "No",
    }

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

    def get_total(self, cost_per_km) -> float:
        total = 0
        total += self.Stationary
        total += self.Welfare_Meal
        total += self.Promotion_Meal
        total += self.Hotel_Rent
        total += self.Connectivity_Charges
        total += self.Travel_Charge
        total += self.Others
        total += self.Personal_Vehicle_Dist * cost_per_km
        return total

    def is_bill_attached(self) -> str:
        if self.Bill_Attached:
            return "Yes"
        return "No"
