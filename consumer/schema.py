import json

from pyflink.common.typeinfo import Types
from pyflink.datastream import MapFunction

CUSTOMER_PRODUCT_SCHEMA = Types.ROW_NAMED(
    [
        "CustomerID",
        "ProductID",
        "Category",
        "Price",
        "Quantity",
        "TransactionDate",
        "ReviewRating",
        "ReviewText",
        "CustomerAge",
        "CustomerGender",
        "Country",
        "DeviceType",
        "BrowsingDuration",
        "PreviousPurchases",
    ],
    [
        Types.STRING(),  # CustomerID
        Types.STRING(),  # ProductID
        Types.STRING(),  # Category
        Types.FLOAT(),  # Price
        Types.INT(),  # Quantity
        Types.STRING(),  # TransactionDate (can be parsed to a Date type if needed)
        Types.FLOAT(),  # ReviewRating
        Types.STRING(),  # ReviewText
        Types.INT(),  # CustomerAge
        Types.STRING(),  # CustomerGender
        Types.STRING(),  # Country
        Types.STRING(),  # DeviceType
        Types.FLOAT(),  # BrowsingDuration
        Types.INT(),  # PreviousPurchases
    ],
)


class ParseAndValidate(MapFunction):
    def map(self, value):
        try:
            # Parse the JSON string into a Python dictionary
            data = json.loads(value)

            # Extract and validate fields
            CustomerID = data.get("CustomerID")
            ProductID = data.get("ProductID")
            Category = data.get("Category")
            Price = float(data.get("Price", 0))
            Quantity = int(data.get("Quantity", 0))
            TransactionDate = data.get("TransactionDate")
            ReviewRating = float(data.get("ReviewRating", 0))
            ReviewText = data.get("ReviewText")
            CustomerAge = int(data.get("CustomerAge", 0))
            CustomerGender = data.get("CustomerGender")
            Country = data.get("Country")
            DeviceType = data.get("DeviceType")
            BrowsingDuration = float(data.get("BrowsingDuration", 0))
            PreviousPurchases = int(data.get("PreviousPurchases", 0))

            # Return the validated and parsed data as a dict
            return {
                "CustomerID": CustomerID,
                "ProductID": ProductID,
                "Category": Category,
                "Price": Price,
                "Quantity": Quantity,
                "TransactionDate": TransactionDate,
                "ReviewRating": ReviewRating,
                "ReviewText": ReviewText,
                "CustomerAge": CustomerAge,
                "CustomerGender": CustomerGender,
                "Country": Country,
                "DeviceType": DeviceType,
                "BrowsingDuration": BrowsingDuration,
                "PreviousPurchases": PreviousPurchases,
            }

        except (ValueError, TypeError, json.JSONDecodeError) as e:
            # Handle parsing errors
            print(f"Error parsing data: {e}, value: {value}")
            return None  # Skip invalid records
