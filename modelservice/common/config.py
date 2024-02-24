import os.path


class Config():
    def __init__(self):
        pass

    def db_folder_path(self):
        return r'C:\Users\Johnson-ITX\Desktop\VAEA\modelservice\database'

    def db_name(self):
        return 'amazon_data.db'

    def table_name(self):
        return 'amazon_data_table'

    def db_path(self):
        return os.path.join(self.db_folder_path(), self.db_name())

    def image_folder_path(self):
        return os.path.join(self.db_folder_path(),'images')

    def model_name(self):
        return "llama2:70b"

    def prompt_info(self):
        info = {
            "product_name":"This is the name of the product.",
            "brand":"This is the brand of the product.",
            "capacity":"This is the capacity of the product. Please fill in Arabic numerals.",
            "colour":"This is the colour of the product.",
            "number_of_reviews":"This is the number of reviews of the product.",
            "wattage":"This is the power wastage of the product.",
            "sale_price":"This is the sale price of the product.",
            "country_of_origin":"This is the origin country of the product.",
            "home_kitchen_rank":"This is the rank of the product in the home kitchen rank.",
            "air_fryers_rank":"This is the rank of the product in the air fryers rank.",
            "Weight":"This is the Weight of the product.",
            "Has_Nonstick_Coating":"This is whether the product contains a non-stick coating.",
            "Material":"This is the material of the product.",
            "Control_Method":"This is the control method of the product.",
            "Recommended_Uses_For_Product":"This is the use of the product which is what users can do with this item.",
            "Manufacturer":"This is the manufacturer of the product.",
            "Model_Name":"This is the model name of the product.",
            "mrp":"This is the suggested retail price of the product.",
            "star_rating":"This is the star rating of the product.",
            "Max_Temperature_Setting":"This is the maximum allowable temperature setting for the product.",
            "Special_Feature":"This is the special feature of the product",
            "description":"This is a summary of the product's features"

        }
        return info



