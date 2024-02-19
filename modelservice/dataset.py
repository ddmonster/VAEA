import copy
from tqdm import tqdm
from datasets import load_dataset
from utils import Data_Base_Util



class Dateset(Data_Base_Util):
    def __init__(self):
        super().__init__()
        self.dbu = Data_Base_Util()
        self.dbu.create_amazon_data_db()

    def insert_data_from_datasets(self):
        dataset = load_dataset("tonypaul2020/amazon_product_data")
        dataset_copy = copy.deepcopy(dataset['train'])
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
            #

            if len(result[1]) == 0:
                self.dbu.insert_data_within_kv(db=self.dbu.db_path(), table_name=self.dbu.table_name(), kv=data_i)

        print('Successful data entry')

if __name__ == '__main__':
    ds = Dateset()
    ds.insert_data_from_datasets()