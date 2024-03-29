
import os
import sqlite3
import sys
import datetime
import re
import json
import random
from modelservice.common.config import Config


'''
class Common_Utils:
    Encapsulation of common tool methods.
'''
class Common_Utils():
    def __init__(self):
        self.dbu = Data_Base_Util()

    # string_2_json: Convert string to json
    def string_2_json(self,json_string):
        pattern = r'\{.*\}'
        match = re.search(pattern, json_string, re.DOTALL)
        if match:
            json_data = match.group()
            try:
                json_data = json.loads(json_data)
                return json_data

            except json.JSONDecodeError as e:
                Exception(f"Error decoding JSON: {e}")
        else:
            Exception("No JSON data match.")

    # tuple_2_json: Given a tuple with individual feature values, match the features in the database with these feature values to form key-value
    # pairs and load them in json.
    def tuple_2_json(self,tuple_string):
        product_json ={}
        result = self.dbu.get_feature_name(db = self.dbu.db_path(),table_name=self.dbu.table_name())
        if result is None:
            raise Exception("Get feature names failed")
        feature_names = result[1]
        for i in zip(feature_names,tuple_string):
            feature = i[0][1]
            feature_value = i[1]
            product_json[feature] = feature_value

        return product_json

    # match_text: Extract the required text from the formatted content generated by LLM by regular matching.
    def match_text(self,text):
        pattern = re.compile(r"```json(.*?)```", re.DOTALL)
        match = pattern.search(text)

        if match:
            matched_content = match.group(1)
            # print("Matched Content")
            pattern = r'\{.*\}'
            match = re.search(pattern, matched_content, re.DOTALL)
            if match:
                print("Match content is JSON.")
                return ''
            else:
                return matched_content+ '\n'
        else:
            print("No match content found.")
            return ''

    # match_product_name: Given the original product name of a product in a database, the refined product name is extracted by regular matching.
    def match_product_name(self,product_name):
        pattern = re.compile(r".*?(?=Fryer)", re.IGNORECASE)
        match = pattern.match(product_name)

        if match:
            matched_text = match.group(0)
            return matched_text+ "Fryer"

        else:
            print("No match product name found.")
            return 'Fryer'

'''
class Rule_Bsed_Language_Util:
    This class is a replica class of some of the functions in Arria for rule-based text generation.
'''
class Rule_Bsed_Language_Util():
    def __init__(self):
        pass

    # random_choose: Character random selection function, given a list, randomly selects an element of the list.
    def random_choose(self,choose_list):
        return choose_list[random.randint(0,len(choose_list)-1)]

    # split_list_2_language: Similar to Arria's asList function, it automatically splits the elements of the list into strings and concatenates the
    # last element with and.
    def split_list_2_language(self,words_list):
        language = ''
        for i,word in enumerate(words_list):
            if len(words_list) == 1:
                language += word

            elif len(words_list) == 2:
                if i == 0:
                    language += f'{word} and '
                else:
                    language += f'{word}'
            else:
                if i <= len(words_list)-3:
                    language += f'{word}, '

                elif i == len(words_list)-2:
                    language += f'{word} and '

                elif i == len(words_list)-1:
                    language += f'{word}'
        return language

    # date_2_language: Given a formatted date string, convert it to a natural language date and allow the user to customize whether the year is needed or have
    # the system randomly decide whether to add the year.
    def date_2_language(self,date_string,isyear='random'):
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        if isyear == 'random':
            num = random.random()
            if num >= 0.5:
                lang_date = date_obj.strftime('%B %#d, %Y')
            else:
                lang_date = date_obj.strftime('%B %#d')

        elif isyear:
            lang_date = date_obj.strftime('%B %#d, %Y')

        else:
            lang_date = date_obj.strftime('%B %#d')

        return lang_date

'''
class Data_Base_Util:
    Database utility classes to implement various database operations.
'''
class Data_Base_Util(Config):
    def __init__(self):
        super().__init__()

    # ts: Time function for displaying the time.
    def ts(self):
        return '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + ']'

    # run_sql: sql statement execution function. This function takes a list of sql statements and can execute multiple sql statements serially.
    def run_sql(self,database, cmd_list):
        b_success = False
        return_value = None

        if database == None:
            return [b_success, return_value]

        cmd = None
        try:
            conn = sqlite3.connect(database)
            c = conn.cursor()
            for cmd in cmd_list:
                cursor = c.execute(cmd)
                return_value = []

                for row in cursor:
                    return_value.append(row)

            conn.commit()

        except Exception as err:
            print(self.ts(), f'Error detected at: {os.path.basename(__file__)}, {__name__}, line', sys._getframe().f_lineno)
            print('  Error:', err)
            print('  Sql cmd:', cmd)

        else:
            b_success = True

        finally:

            try:
                c.close()
            except:
                pass

            try:
                conn.close()
            except:
                pass

            if not b_success:
                print("Warning in run_sql: operation failed.")
                print(f"cmd_list = {cmd_list}, return_value = {return_value}")

        return [b_success, return_value]

    # create_amazon_data_db: Create amazon_data.db
    def create_amazon_data_db(self):

        is_success, return_value = self.run_sql(self.db_path(),
                                                cmd_list=[f'''CREATE TABLE IF NOT EXISTS "{self.table_name()}" (
                                                               "id"	CHAR(64) DEFAULT NULL,
                                                               "date"	CHAR(64) DEFAULT NULL,
                                                               "urls"	CHAR(64) DEFAULT NULL,
                                                               "product_name"	CHAR(64) DEFAULT NULL,
                                                               "brand"	CHAR(64) DEFAULT NULL,
                                                               "star_rating"	CHAR(64) DEFAULT NULL,
                                                               "number_of_reviews"	CHAR(64) DEFAULT NULL,
                                                               "mrp"	CHAR(64) DEFAULT NULL,
                                                               "sale_price"	CHAR(64) DEFAULT NULL,
                                                               "colour"	CHAR(64) DEFAULT NULL,
                                                               "capacity"	CHAR(64) DEFAULT NULL,
                                                               "wattage"	CHAR(64) DEFAULT NULL,
                                                               "country_of_origin"	CHAR(64) DEFAULT NULL,
                                                               "home_kitchen_rank"	CHAR(64) DEFAULT NULL,
                                                               "air_fryers_rank"	CHAR(64) DEFAULT NULL,
                                                               "technical_details"	CHAR(64) DEFAULT NULL,
                                                               "description"	CHAR(64) DEFAULT NULL,
                                                               "asin"	CHAR(64) DEFAULT NULL,
                                                               "capacity_1"	CHAR(64) DEFAULT NULL,
                                                               "Weight"	CHAR(64) DEFAULT NULL,
                                                               "Has_Nonstick_Coating"	CHAR(64) DEFAULT NULL,
                                                               "Material"	CHAR(64) DEFAULT NULL,
                                                               "Manufacturer"	CHAR(64) DEFAULT NULL,
                                                               "Control_Method"	CHAR(64) DEFAULT NULL,
                                                               "Model_Name"	CHAR(64) DEFAULT NULL,
                                                               "Recommended_Uses_For_Product"	CHAR(64) DEFAULT NULL,
                                                               "Special_Feature"	CHAR(64) DEFAULT NULL,
                                                               "Max_Temperature_Setting"	CHAR(64) DEFAULT NULL,
                                                               "Imported_By"	CHAR(64) DEFAULT NULL
                                                           ); '''])

        if not is_success:

            return None

        else:
            return [is_success, return_value]

    # insert_data_within_kv: Given a dictionary where the keys are database column names and the values are the values to be inserted, this function
    # will perform database interpolation based on the key-value pairs.
    def insert_data_within_kv(self,db,table_name,kv):
        key_body = ''
        value_body = ''
        for key,value in kv.items():
            key_body += (str(key)+',')
            value_str = str(value)
            if "'" in str(value):
                value_str = str(value).replace("'",'"')

            if 'None' in str(value):
                value_str = str(value).replace('None','NULL')
            #
            value_body += ("'"+value_str+"'"+',')

        is_success,return_value =self.run_sql(db, cmd_list=[f'''INSERT INTO {table_name} ({key_body[:-1]}) VALUES ({value_body[:-1]})'''])

        if not is_success:

            return None

        else:
            return [is_success, return_value]

    # select_data_within_kv: Given a dictionary, where the keys are database column names and the values are the values that need to be inserted into
    # the query, this method queries all the rows in the database that match the conditions by using the specified key-value pairs as conditions.
    def select_data_within_kv(self,db,table_name,kv):

        kv_body = ''

        for k, v in kv.items():
            kv_body += f'{k}="{v}" AND '

        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''SELECT * FROM {table_name} WHERE {kv_body[:-5]}'''])
        if not is_success:

            return None

        else:
            return [is_success, return_value]

    # select_column_data_within_kv: Given a column name and a set of key-value pairs for a query condition, query the column name for all values that match
    # the key-value pair condition.
    def select_column_data_within_kv(self,db,table_name,column_name,kv):

        kv_body = ''

        for k, v in kv.items():
            kv_body += f'{k}="{v}" AND '

        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''SELECT {column_name} FROM {table_name} WHERE {kv_body[:-5]}'''])
        if not is_success:

            return None

        else:
            return [is_success, return_value]

    # select_data_within_column: Given a column name, query all values under that column name.
    def select_data_within_column(self,db,table_name,column_name):

        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''SELECT {column_name} FROM {table_name}'''])
        if not is_success:
            return None

        else:
            return [is_success, return_value]

    # get_data_num: Query how many data.
    def get_data_num(self,db,table_name):

        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''SELECT COUNT(*) FROM  {table_name}'''])
        if not is_success:
            return None

        else:
            return [is_success, return_value]

    # get_a_row: Given a row index number, returns all data for that row.
    def get_a_row(self,db,table_name,row_num):

        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''SELECT * FROM {table_name} LIMIT 1 OFFSET {row_num}'''])
        if not is_success:
            return None

        else:
            return [is_success, return_value]

    # get_feature_name: Query all feature names, i.e. column names.
    def get_feature_name(self,db,table_name):
        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''PRAGMA table_info({table_name})'''])
        if not is_success:
            return None

        else:
            return [is_success, return_value]

    # get_columnB_from_columnA: Given the value of column A, query all the values of column B that satisfy the conditions for the value of column A.
    def get_columnB_from_columnA(self,db,table_name,columnB_name,columnA_name,columnA_value):
        is_success, return_value = self.run_sql(db,
                                                cmd_list=[f'''SELECT {columnB_name} FROM {table_name} WHERE {columnA_name}="{columnA_value}"'''])
        if not is_success:
            return None

        else:
            return [is_success, return_value]