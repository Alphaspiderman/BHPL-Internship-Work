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

    hidden_fields = ["Id", "Employee_Id"]

    convert_fields = {
        "Date_Of_Expense": lambda x: x.strftime("%Y-%m-%d"),
        "Stationary": lambda x: float(x),
        "Welfare_Meal": lambda x: float(x),
        "Promotion_Meal": lambda x: float(x),
        "Hotel_Rent": lambda x: float(x),
        "Connectivity_Charges": lambda x: float(x),
        "Travel_Charge": lambda x: float(x),
        "Others": lambda x: float(x),
        "Bill_Attached": lambda x: "Yes" if x else "No",
        "Personal_Vehicle_Dist": lambda x: float(x),
    }

    def __init__(self, data, cost_per_km_four_wheeler, cost_per_km_two_wheeler):
        self.car_km_cost = cost_per_km_four_wheeler
        self.bike_km_cost = cost_per_km_two_wheeler
        for idx, field in enumerate(self.fields):
            setattr(self, field, data[idx])

    def to_dict(self) -> dict:
        return {field: getattr(self, field) for field in self.fields}

    def get_data(self, show_id: bool = False, show_file_names: bool = False) -> dict:
        data = self.to_dict()
        hide = self.hidden_fields.copy()
        if show_id:
            hide.remove("Id")
        for field in hide:
            data.pop(field, None)
        for field, convert in self.convert_fields.items():
            data[field] = convert(data[field])
        if show_file_names and self.is_bill_attached() == "Yes":
            data["Bill_Attached"] = self.Bill_Attached
        return data

    @classmethod
    def get_schema(self, show_id: bool = False) -> dict:
        schema = self.fields.copy()
        hide = self.hidden_fields.copy()
        if show_id:
            hide.remove("Id")
        for field in hide:
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
        if self.Vehicle_Type == "Car":
            return self.Personal_Vehicle_Dist * self.car_km_cost
        elif self.Vehicle_Type == "Bike":
            return self.Personal_Vehicle_Dist * self.bike_km_cost
        else:
            return 0.00

    def get_vehicle_type(self) -> str:
        if self.Vehicle_Type:
            return self.Vehicle_Type
        return "N/A"

    def get_data_with_id(self) -> dict:
        data = self.to_dict()["Id"] = self.Id
        return data
