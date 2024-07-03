class Location:
    fields = [
        "Store_Code",
        "Store_Name",
        "Posist_Store_Name",
        "Ownership_Type",
        "Local_Address",
        "City",
        "State_Name",
        "Region_Internal",
        "Postal_Code",
        "Champs_Number",
        "Primary_Brand_Channel",
        "Facility_Type",
        "Ordering_Methods",
        "Store_Type",
        "Store_Phone",
        "Store_Email",
        "Status",
        "Latitude",
        "Longitude",
        "Store_Open_Date",
        "Posit_Live_Date",
        "Seat_Count",
        "Local_Org_Name",
        "Franchisee_id",
        "Temp_Close_Date",
        "Reopen_Date",
        "Store_Closure_Date",
        "Sunday_Open",
        "Sunday_Close",
        "Monday_Open",
        "Monday_Close",
        "Tuesday_Open",
        "Tuesday_Close",
        "Wednesday_Open",
        "Wednesday_Close",
        "Thursday_Open",
        "Thursday_Close",
        "Friday_Open",
        "Friday_Close",
        "Saturday_Open",
        "Saturday_Close",
        "Market_Name",
        "Area_Name",
        "Coach_ID",
        "Ip_Range_Start",
        "Ip_Range_End",
        "Subnet",
        "Static_Ip",
        "Link_ISP",
        "Link_Type",
    ]

    hidden_fields = [
        "Posist_Store_Name",
        "Ownership_Type",
        "Local_Address",
        "Champs_Number",
        "Primary_Brand_Channel",
        "Facility_Type",
        "Ordering_Methods",
        "Sunday_Open",
        "Sunday_Close",
        "Monday_Open",
        "Monday_Close",
        "Tuesday_Open",
        "Tuesday_Close",
        "Wednesday_Open",
        "Wednesday_Close",
        "Thursday_Open",
        "Thursday_Close",
        "Friday_Open",
        "Friday_Close",
        "Saturday_Open",
        "Saturday_Close",
    ]
    IT_only_fields = [
        "Ip_Range_Start",
        "Ip_Range_End",
        "Subnet",
        "Static_Ip",
        "Link_ISP",
        "Link_Type",
    ]

    def __init__(self, data):
        for idx, field in enumerate(self.fields):
            setattr(self, field, data[idx])

    def to_dict(self) -> dict:
        return {field: getattr(self, field) for field in self.fields}

    def get_data(self, is_IT: bool) -> dict:
        data = self.to_dict()
        for field in self.hidden_fields:
            data.pop(field)
        if not is_IT:
            for field in self.IT_only_fields:
                data.pop(field)
        return data

    def get_schema(self, is_IT) -> dict:
        schema = self.fields
        for field in self.hidden_fields:
            schema.remove(field)
        if not is_IT:
            for field in self.IT_only_fields:
                schema.remove(field)
        return schema
