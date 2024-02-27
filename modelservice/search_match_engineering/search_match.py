import numpy as np
from modelservice.common.utils import Data_Base_Util
from fuzzywuzzy import process


'''
class Search_Match:
    Here we implement an attention-based product search engine.

'''
class Search_Match():
    def __init__(self):
        self.dbu=Data_Base_Util()

    # Algorithmic process
    # 1. First we obtained a list of JSON key-value pairs from LLM containing 15 features.
    # 2. Precision Search: Then we try to do an accurate search directly based on the product_name in the json, and output the data directly after searching.
    # 3. Fuzzy search:However it is difficult to get a direct hit in the vast majority of cases. We then obtain the number N of data entries in the database
    #    and create an N x 15 all -1 initial attention matrix M.
    # 4. The key-value pairs in a JSON feature table can be viewed as a 1 x 15 matrix M_1, except that the matrix is populated with strings.
    # 5. We search N x 15 data from the database based on the given features to form an N x 15 string-filled feature matrix M_2.
    # 6. We then multiply M_1 and M_2 with a special similarity algorithm, the Levenshtein Distance algorithm.
    # 7. It ends up with an Nx15 matrix of numbers, where the filled numbers are similarity scores, that is, how similar a feature of each product
    #    is to a given input feature. This value is also the attention value of that product for a given feature.
    # 8. This algorithm writes the values to the initial matrix M for each completed computation, resulting in an Nx15 numeric matrix M', where the filled
    #    numbers are the similarity scores, i.e., the degree of similarity of a given feature of each product to a given input feature. This value is also
    #    the attention value of that product for a given feature.
    # 9. The reason we set the value of the initial matrix to -1 is to distinguish which features the algorithm uses for the computation. Since some features
    #    cannot be extracted at the time of extraction, such features without values will no longer be included in subsequent calculations.
    # 10. After obtaining the attention matrix M', we need to prioritize the various types of features and we use two grading algorithms for different input situations.
    #
    #
    #     ---Weighted Attention Algorithm:  In this algorithm, we calculate the score of the feature based on the data in each column, weighted, which is between 0 and 100,
    #                                    and we end up with 15 feature values, which are then weighted to find the weight of each feature value as the attention value of
    #                                    the feature.
    #
    #     ---Sorting Attention Algorithms: This algorithm we sort 15 features based on the weighted attention algorithm. After sorting, we subtract 15 from the sorted ordinal
    #                                    number and divide by 15 to force this value to be the attention value for that feature.
    #
    #
    #     The above two algorithms in order to due to different situations. The weighted attention algorithm is more sensitive when the weights between features differ significantly.
    #     However, when the feature weights are all quite similar to each other, it is difficult to select the best term. In this case, the second algorithm, the ranked attention algorithm,
    #     is used, which forces polarization of the differences in feature attention values, especially when there are fewer features available for computation. This can force the matching
    #     priority of the head features to be raised and the priority of the tail features to be weakened, so that the final matched product has at least some features that are very much in
    #     line with what the user wants.
    #
    # 11. In practice, the system randomly selects an algorithm for matching in order to enhance diversity. When matching, the attention value of each piece of data is multiplied by the
    #    eigenvalue weights to calculate the final attention value of each piece of data. The system selects the piece of data with the largest attention value as the matching output.

    # get_all_product_feature_value_in_one_column: Gets all values for a feature.
    def get_all_product_feature_value_in_one_column(self,column_name):
        [is_success, return_value] = self.dbu.select_data_within_column(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                                   column_name=column_name)
        if is_success:
            return return_value

        else:
            raise Exception(f'Search all product value in column {column_name} error')

    # match_product_feature_value: Calculate the similarity of all values to a given value under a certain feature, also known as the attention value. This calculation is a process of multiplying a character by a character
    # to get a number. It is the key to converting a character matrix to a number matrix.
    def match_product_feature_value(self,feature_name,feature_value):
        all_product_value = self.get_all_product_feature_value_in_one_column(column_name=feature_name)
        score_list = []
        for product in all_product_value:
            match, score = process.extractOne(feature_value, [product])
            score_list.append(score)

        return np.asarray(score_list)

    # create_attention_matrix: Creates an N x 15 -1 initial matrix. And fill in the attention values for each feature
    def create_attention_matrix(self,feature_json,data_num):
        i = 0
        init_matrix = np.full((data_num, 15), -1)
        for k,v in feature_json.items():
            if ((v is None)|(v=='')):
                i+=1
                continue

            score_list=self.match_product_feature_value(feature_name=k,feature_value=v)
            init_matrix[:, i] = score_list
            i+=1

        return init_matrix

    # get_feature_weights: Weighted Attention Feature Hierarchy Algorithm and Ranked Attention Feature Hierarchy Algorithm.
    # The system chooses one randomly.
    def get_feature_weights(self,matrix):
        matrix_weights = matrix / np.sum(matrix, axis=0)
        weighted_average = np.sum(matrix * matrix_weights, axis=0)
        weighted_average = np.where(weighted_average==-1,0,weighted_average)
        random_number = np.random.rand()
        if random_number<= 0.5:
            feature_weight= weighted_average / np.sum(weighted_average)

        else:
            feature_weight = (np.argsort(weighted_average)+1)/len(weighted_average)
        return feature_weight

    # get_attention_item: The feature values of each row of data are multiplied by the feature weights and a weighted sum is derived, with the row with the largest
    # sum as the final best match.
    def get_attention_item(self,attention_matrix):
        feature_weight = self.get_feature_weights(matrix=attention_matrix)
        row_sums = np.average(attention_matrix, axis=1, weights=feature_weight)
        max_attention_index = np.argmax(row_sums)
        result = self.dbu.get_a_row(db=self.dbu.db_path(),table_name=self.dbu.table_name(),row_num=max_attention_index)
        if result is None:
            raise Exception('Get most attention item failed')

        else:
            print(f'Best result is: {result[1][0]}')
            return result[1][0]

    # fuzzy_matching: Encapsulation methods for fuzzy matching.
    def fuzzy_matching(self,feature_result,data_num):
        attention_matrix = self.create_attention_matrix(feature_json=feature_result, data_num=data_num)
        best_item = self.get_attention_item(attention_matrix=attention_matrix)
        return best_item

    # exact_match: An encapsulation method for precise matching. Realized by directly querying the database.
    def exact_match(self,product_name):
        result=self.dbu.select_data_within_kv(db = self.dbu.db_path(),table_name=self.dbu.table_name(),kv = {'product_name':f'{product_name}'})
        if result is None:
            raise Exception('Exact matching failed')

        else:
            match_result = result[1]
            if len(match_result)>0:
                return match_result[0]

            else:
                return None

    # match_product: Product matching encapsulation method.
    def match_product(self,feature_result,data_num):
        product_name = feature_result["product_name"]
        if (product_name is None) | (product_name == ""):
            best_item = self.fuzzy_matching(feature_result=feature_result,data_num=data_num)
            print('Product name is None')
            return best_item

        else:
            exact_match = self.exact_match(product_name=product_name)
            if exact_match is None:
                best_item = self.fuzzy_matching(feature_result=feature_result, data_num=data_num)
                print('Cannot match product name using exact match, turning to fuzzy match')
                return best_item

            else:
                print('Can match product name using exact match')
                return exact_match


