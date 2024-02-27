import copy
import os.path
from tqdm import tqdm
from datasets import load_dataset

from modelservice.common.utils import Data_Base_Util


'''
class Dateset: 
    Dataset Building Classes
'''
class Dateset(Data_Base_Util):
    def __init__(self):
        super().__init__()
        self.dbu = Data_Base_Util()
        self.dbu.create_amazon_data_db()

    # insert_data_from_datasets: Write datasets brought in from outside to the database to build local datasets.
    def insert_data_from_datasets(self):
        dataset = load_dataset("tonypaul2020/amazon_product_data")
        dataset_copy = copy.deepcopy(dataset['train'])
        try:
            for i in tqdm(range(len(dataset_copy)), desc="Data Entry", unit="item"):
                data_i =dataset_copy[i]
                for k, v in data_i.copy().items():
                    new_k = k
                    if ' ' in k:
                        new_k = k.replace(' ', '_')
                        data_i[new_k] = data_i.pop(k)

                    if k == 'Capacity':
                        new_k = 'capacity_1'
                        data_i[new_k] = data_i.pop(k)

                    if isinstance(v, float):
                        data_i[new_k] = str(v)

                    elif v is None:
                        data_i[new_k] = 'None'

                data_id = data_i['urls'].split('/')[-1]
                data_i['id'] = data_id
                kv= {'id': data_id}
                result = self.dbu.select_data_within_kv(db=self.dbu.db_path(), table_name=self.dbu.table_name(), kv=kv)

                if len(result[1]) == 0:
                    self.dbu.insert_data_within_kv(db=self.dbu.db_path(), table_name=self.dbu.table_name(), kv=data_i)
        except Exception as e:
            raise Exception(f'Failed to create dataset. {e}')

        else:
            print('Success to create dataset.')

    # make_dataset: This method automatically checks the existence of the database and the contents of the database
    # to determine whether the database needs to be created and written to.
    def make_dataset(self):
        if os.path.exists(self.db_path()):
            result = self.dbu.get_data_num(db=self.dbu.db_path(),table_name=self.table_name())
            if result is None:
                raise Exception('Check data num failed')
            else:
                num = result[1][0][0]
                if num == 0:
                    self.insert_data_from_datasets()

                    data_num = self.dbu.get_data_num(db=self.dbu.db_path(),table_name=self.table_name())
                    if data_num is None:
                        raise Exception('Check data num failed')
                    else:
                        return data_num[1][0][0]

                else:
                    print('Dataset has been created before.')
                    data_num = self.dbu.get_data_num(db=self.dbu.db_path(), table_name=self.table_name())
                    if data_num is None:
                        raise Exception('Check data num failed')
                    else:
                        return data_num[1][0][0]

        else:
            self.insert_data_from_datasets()
            data_num = self.dbu.get_data_num(db=self.dbu.db_path(), table_name=self.table_name())
            if data_num is None:
                raise Exception('Check data num failed')
            else:
                return data_num[1][0][0]
