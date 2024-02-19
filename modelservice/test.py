import copy
import os
import sqlite3
import sys
import datetime
from config import Config





class Data_Base_Util(Config):
    def __init__(self):
        super().__init__()

    def ts(self):
        """
        # 返回当前时间的字符串，精度【ms】
        # 可通过fromisoformat()函数转换为datetime对象
        # 如datetime.datetime.fromisoformat('2022-07-02 05:03:24.123')
        """
        return '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + ']'

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

            # 安全关闭资源
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

    def create_total_task_record_db(self):
        # total_task_load表：总负载均衡表，汇总每个节点的数据情况
        is_success, return_value = self.run_sql(self.db_path(),
                                                cmd_list=[f'''CREATE TABLE IF NOT EXISTS "{self.table_name()}" (
                                                               "task_id"	CHAR(64) DEFAULT NULL,
                                                               "request"	CHAR(64) DEFAULT NULL,
                                                               "response"	CHAR(64) DEFAULT NULL,
                                                               "status"	CHAR(64) DEFAULT NULL,
                                                               "send_topic"	CHAR(64) DEFAULT NULL,
                                                               "send_host"	CHAR(64) DEFAULT NULL,
                                                               "send_port"	CHAR(64) DEFAULT NULL,
                                                               "send_groupid"	CHAR(64) DEFAULT NULL,
                                                               "receive_topic"	CHAR(64) DEFAULT NULL,
                                                               "receive_host"	CHAR(64) DEFAULT NULL,
                                                               "receive_port"	CHAR(64) DEFAULT NULL,
                                                               "receive_groupid"	CHAR(64) DEFAULT NULL,
                                                               "retry_time"	CHAR(64) DEFAULT NULL,
                                                               "time_stamp"	CHAR(64) DEFAULT NULL,
                                                               "isack"	CHAR(64) DEFAULT NULL
                                                           ); '''])

        if not is_success:
            # 待增加失败后的操作
            return None

        else:
            return [is_success, return_value]

    def create_amazon_data_db(self):
        # total_task_load表：总负载均衡表，汇总每个节点的数据情况
        is_success, return_value = self.run_sql(self.db_path(),
                                                cmd_list=[f'''CREATE TABLE IF NOT EXISTS "{self.table_name()}" (
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
            # 待增加失败后的操作
            return None

        else:
            return [is_success, return_value]

    # def create_total_task_load_db(self):
    #     # total_task_load表：总负载均衡表，汇总每个节点的数据情况
    #     is_success,return_value = self.run_sql(self.main_node_database_path(),
    #                                            cmd_list=[f'''CREATE TABLE IF NOT EXISTS "{self.total_task_load()}" (
    #                                                         "topic"	CHAR(64) DEFAULT NULL,
    #                                                         "compute_topic"	CHAR(64) DEFAULT NULL,
    #                                                         "host"	CHAR(64) DEFAULT NULL,
    #                                                         "port"	CHAR(64) DEFAULT NULL,
    #                                                         "groupid"	CHAR(64) DEFAULT NULL,
    #                                                         "current_task_num" CHAR(64) DEFAULT NULL,
    #                                                         "time_stamp"	CHAR(64) DEFAULT NULL
    #                                                     ); '''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    #
    # def create_sub_task_load_db(self,algo_process_name):
    #     # sub_task_load表：每个子节点的每个并行算法服务对应的任务负载队列表
    #     #status是任务状态，0表示等待，1表示执行中，完成的话直接删除没有状态，2表示进程挂了
    #     is_success,return_value = self.run_sql(self.sub_node_database_path(),
    #                                            cmd_list=[f'''CREATE TABLE IF NOT EXISTS "{self.sub_task_load(num=algo_process_name)}" (
    #                                                          "task_id"	CHAR(64) DEFAULT NULL,
    #                                                          "task_type"	CHAR(64) DEFAULT NULL,
    #                                                          "request" CHAR(64) DEFAULT NULL,
    #                                                          "status" CHAR(64) DEFAULT NULL,
    #                                                          "time_stamp" CHAR(64) DEFAULT NULL
    #                                                     ); '''])
    #
    #     if not is_success:
    #         #待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    #
    # def create_sub_task_info_db(self):
    #     # sub_task_load表：每个子节点的每个并行算法服务对应的任务负载队列表
    #     #status是任务状态，0表示等待，1表示执行中，完成的话直接删除没有状态，2表示进程挂了
    #     is_success,return_value = self.run_sql(self.sub_node_database_path(),
    #                                            cmd_list=[f'''CREATE TABLE IF NOT EXISTS "{self.sub_info_report()}" (
    #                                                          "task_id"	CHAR(64) DEFAULT NULL,
    #                                                          "response" CHAR(64) DEFAULT NULL,
    #                                                          "time_stamp" CHAR(64) DEFAULT NULL
    #                                                     ); '''])
    #
    #     if not is_success:
    #         #待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    #
    # def check_all_table_name(self,db):
    #     is_success, return_value = self.run_sql(db,
    #                                             cmd_list=[f'''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name'''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    # def check_curr_all_subprocess_task_load(self,num):
    #     is_success, return_value = self.run_sql(self.sub_node_database_path(),
    #                                             cmd_list=[f'''SELECT * FROM {self.sub_task_load(num=num)}'''])
    #
    #     if not is_success:
    #         #待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success,return_value]
    #
    # def check_curr_all_subprocesses_info(self):
    #     is_success, return_value = self.run_sql(self.sub_node_database_path(),
    #                                             cmd_list=[f'''SELECT * FROM {self.sub_info_report()}'''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    #
    # def check_curr_all_nodes_load(self):
    #     is_success, return_value = self.run_sql(self.main_node_database_path(),
    #                                             cmd_list=[f'''SELECT * FROM {self.total_task_load()}'''])
    #
    #     if not is_success:
    #         #待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success,return_value]
    #
    # def count_info_num(self,db,table_name):
    #     is_success, return_value = self.run_sql(db,
    #                                             cmd_list=[f'''SELECT COUNT(*) from {table_name}'''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    # def select_data_within_kv(self,db,table_name,kv):
    #
    #     kv_body = ''
    #
    #     for k, v in kv.items():
    #         kv_body += f'{k}="{v}" AND '
    #
    #     is_success, return_value = self.run_sql(db,
    #                                             cmd_list=[f'''SELECT * FROM {table_name} WHERE {kv_body[:-5]}'''])
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    #
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
            # 待增加失败后的操作
            return None

        else:
            return [is_success, return_value]
    #
    # def delete_data_within_kv(self,db,table_name,kv):
    #     kv_body = ''
    #     for key,value in kv.items():
    #         #
    #         # key_str = str(key)
    #         # value_str = str(value)
    #         # if "'" in key_str:
    #         #     key_str = key_str.replace("'",'"')
    #         #
    #         # if "'" in value_str:
    #         #     value_str = value_str.replace("'", '"')
    #
    #         kv_body += f"{key}='{value}' AND "
    #         # kv_body += (key_str+'='+value_str+' AND ')
    #
    #     is_success, return_value = self.run_sql(db, cmd_list=[f'DELETE FROM {table_name} WHERE {kv_body[:-5]}'])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    # def get_data_by_row(self,db,table_name,end_row=1):
    #     is_success, return_value = self.run_sql(db, cmd_list=[
    #         f'''SELECT * FROM {table_name} LIMIT {end_row}'''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    # def change_data_within_kv(self,db,table_name,src_kv,target_kv):
    #
    #     src_body=''
    #     target_body =''
    #     for k, v in src_kv.items():
    #         v= str(v)
    #         if "'" in v:
    #             v=v.replace("'",'"')
    #         src_body += f'''{k}='{v}' AND '''
    #
    #     for k, v in target_kv.items():
    #         v = str(v)
    #         if "'" in v:
    #             v = v.replace("'", '"')
    #         target_body += f'''{k}='{v}', '''
    #
    #     is_success,return_value =self.run_sql(db, cmd_list=[f'''UPDATE {table_name} set {target_body[:-2]} WHERE {src_body[:-5]}'''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]
    #
    # def clear_db(self,db,table_name):
    #     is_success,return_value =self.run_sql(db, cmd_list=[f'''DELETE FROM {table_name}'''])
    #
    #     if not is_success:
    #         # 待增加失败后的操作
    #         return None
    #
    #     else:
    #         return [is_success, return_value]





if __name__ == '__main__':
    from datasets import load_dataset

    dbu = Data_Base_Util()
    dbu.create_amazon_data_db()

    dataset = load_dataset("tonypaul2020/amazon_product_data")
    print(dataset['train'][0], len(dataset['train']))
    dataset_1 = copy.deepcopy(dataset['train'])
    print(dataset_1[0].keys(),len(dataset_1[0].keys()))
    for dataset_1_i in dataset_1:

    # dataset_1_0['url1'] = dataset_1_0.pop('urls')
    #
    # print(dataset_1_0['url1'])
        for k,v in dataset_1_i.copy().items():
            new_k = k
            if ' ' in k:
                new_k = k.replace(' ','_')
                dataset_1_i[new_k] = dataset_1_i.pop(k)

            if k == 'Capacity':
                new_k = 'capacity_1'
                dataset_1_i[new_k] = dataset_1_i.pop(k)
        #
            if isinstance(v,float):
                dataset_1_i[new_k]= str(v)

            elif v is None:
        #
                dataset_1_i[new_k] = 'None'

        print(dataset_1_i)
        #


        dbu.insert_data_within_kv(db=dbu.db_path(),table_name=dbu.table_name(),kv=dataset_1_i)





    # dbc = Data_Base_Config()
    # db = 0
    # sub_node_name = 'SubManager2'
    # algo_name = 'algo3'
    # # aa =dbu.find_data_within_kv(dbc.main_node_database_path(),'total_task_load','topic','node3')
    # # print(aa)
    #
    # kv = {"topic":"compute_node_2",
    #         "host": "127.0.0.1",
    #         "port": "9092",
    #         "groupid":"xx",
    #         "current_task_num":'2',
    #       "time_stamp":dbu.ts()}
    # print(dbu.ts())
    # cu=Common_Util()
    # cu.create_task_file('1234')
    #
    # aa = dbu.delete_data_within_kv(db= dbu.sub_node_database_path(),table_name='sub_task_load_0',kv={'task_id':'aa','time_stamp':'123'})
    # print(aa)
    # aa = dbu.get_data_by_row(db=dbu.sub_node_database_path(), table_name='sub_task_load_0'
    #                                )
    # print(aa)
    # print(dbu.ts())
    # aa = dbu.check_all_table_name(dbu.sub_node_database_path())
    # print(aa)
    # dbu.create_sub_task_info_db()
    # bb = dbu.count_info_num(db = dbu.sub_node_database_path(),table_name='sub_task_load_4')
    # print(bb)
    # bb = dbu.insert_data_within_kv(dbc.main_node_database_path(),dbc.total_task_load(),kv)
    # BB= dbu.change_data_within_kv(db = dbc.main_node_database_path(),table_name=dbc.total_task_record(),
    #                               src_kv={'task_id':'asd','send_topic':'compute_node_2'},
    #                               target_kv={'retry_time':'2','send_port':'xxx'})
    # print(dbu.compute_early_from_now('[2023-06-01 09:47:32,790]'))
    # cc = dbu.delete_data_within_kv(db=dbc.main_node_database_path(),table_name=dbc.total_task_load(),kv = kv)
    # dbu.create_total_task_load_db()
    # dbu.create_sub_task_load_db(sub_node_task_queue_table_name=sub_node_name,algo_process_name=algo_name)
    # [is_success,return_value]=dbu.check_curr_all_nodes_load()
    # print(return_value)
    # print(return_value)