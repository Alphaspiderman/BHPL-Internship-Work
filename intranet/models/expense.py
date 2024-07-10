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
        "Vehicle_Type",
        "Reason",
    ]

    hidden_fields = ["Id"]

    convert_fields = {
        "Date_Of_Expense": lambda x: x.strftime("%Y-%m-%d"),
        "Receipt_Attached": lambda x: "Yes" if x else "No",
    }

    def __init__(self, data, cost_per_km_four_wheeler, cost_per_km_two_wheeler):
        self.cost_per_km_four_wheeler = cost_per_km_four_wheeler
        self.cost_per_km_two_wheeler = cost_per_km_two_wheeler
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

    def get_total(self) -> float:
        total = 0.0
        total += float(self.Stationary)
        total += float(self.Welfare_Meal)
        total += float(self.Promotion_Meal)
        total += float(self.Hotel_Rent)
        total += float(self.Connectivity_Charges)
        total += float(self.Travel_Charge)
        total += float(self.Others)
        total += self.get_personal_vehicle_comp()
        return total

    def is_bill_attached(self) -> str:
        if self.Bill_Attached:
            return "Yes"
        return "No"

    def get_personal_vehicle_comp(self) -> float:
        if self.Vehicle_Type == "4 Wheeler":
            return self.Personal_Vehicle_Dist * self.cost_per_km_four_wheeler
        elif self.Vehicle_Type == "2 Wheeler":
            return self.Personal_Vehicle_Dist * self.cost_per_km_two_wheeler
        else:
            return 0.00

    def get_vehicle_type(self) -> str:
        if self.Vehicle_Type:
            return self.Vehicle_Type
        return "N/A"
