from langchain.output_parsers import ResponseSchema
from modelservice.product_text_generation_engineering.planning import Documentation_Planning
from modelservice.product_text_generation_engineering.planning import Micro_Planning
from modelservice.common.config import Config
from modelservice.model.model import LLM_Model
from modelservice.common.utils import Common_Utils

'''
class LLM_Genertion_Text:
    This class encapsulates a method for generating product introduction text based on LLAMA2.
'''
class LLM_Genertion_Text(LLM_Model):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.dp = Documentation_Planning()
        self.mp = Micro_Planning()
        self.config = Config()
        self.cu = Common_Utils()

    # ****************************************************************************************************************************************
    # generate_product_text: This method is used to generate product presentation text based on document planning and microplanning.
    # First, given the json of product data and the grouping of product features (similar features will be grouped together), each
    # feature group will be divided into natural segments attributed according to the planning in Documentation_Planning(). That is to say,
    # according to the existing features and document planning, which natural segments should be generated in this paper, and in which
    # paragraphs of these natural segments, which feature points should be included in the introduction. Thereafter, the feature points
    # and feature values that should be included in each natural paragraph are assembled into ResponseSchema, which is poured into LLAMA2,
    # so that LLAMA2 can generate text paragraph by paragraph. Finally, these natural segments are stitched together.
    # ******************************************************************************************************************************************
    def generate_product_text(self,feature_group_json,product_json):

        order_list = self.get_order_from_product_json(feature_group_json=feature_group_json) # Get the distribution of natural segments in this introduction
        product_total_text = ''
        product_name = self.cu.match_product_name(product_name=product_json['product_name'])
        for i,order in enumerate(order_list):
        #  Obtain the paragraph ordering distribution of this article (In document planning, the complete article contains 7 paragraphs, but after feature
        #  filtering, it may be less than 7 paragraphs. So here we get the ordering of all paragraphs, how many in total and which ones respectively)

            try:
                # In paragraph ordering, the first paragraph needs to be placed as the opening paragraph and the last paragraph as the closing paragraph.
                # However, please note that the first paragraph does not necessarily correspond to paragraph 1 in the original document planning, and the
                # last paragraph does not necessarily correspond to paragraph 6 in the document planning, so it needs to be forced to the beginning or the end.

                if i == 0:
                    paragraph = f'self.dp.paragraph_{order}(is_opening=True,is_closing=False)'

                elif i == len(order_list)-1:
                    paragraph = f'self.dp.paragraph_{order}(is_opening=False,is_closing=True)'

                else:
                    paragraph = f'self.dp.paragraph_{order}(is_opening=False,is_closing=False)'

                # Using the eval function, the string is activated so that we can get the feature points of which generations of introductions the segment should contain
                group_name,group_intro = eval(paragraph)
                group_feature_contain = eval(f'self.mp.{group_name}()')
                group_feature_json = {}
                response_schemas = []

                # Compose a ResponseSchema of the currently available feature points and feature values within a paragraph.
                for feature in group_feature_contain:
                    if feature in feature_group_json[group_name]:
                        group_feature_json[feature]=product_json[feature]
                        schema = ResponseSchema(name=feature, description=self.config.prompt_info()[feature])
                        response_schemas.append(schema)

                # Generate paragraphs and match them from the output.
                paragraph_text_result = self.ollama_generation_one_paragraph(response_schemas=response_schemas,product_name=product_name,
                                                     paragraph_intro=group_intro,input_json=group_feature_json)

                paragraph_text_result = self.cu.match_text(text=paragraph_text_result)
                print(paragraph_text_result)
                product_total_text += paragraph_text_result

            except Exception as e:
                print(f'Exception occured {e}')
                continue

        # The seventh paragraph is RULE-BASED generated, which reads the data directly from the description column in the database and
        # tries to turn it into a list, listing summaries by point. However, since the dataset is not cleaned, this operation may fail
        # due to irregularities. If it fails, it does not affect the stability of the system and will output the current text that has
        # been generated.
        try:
            paragraph_7 = eval(f'self.mp.{self.dp.paragraph_7()}()')
            paragraph_7_data = eval(product_json[paragraph_7[0]])
            product_total_text += f"Let's review this {product_name}:\n"

            for sentence in paragraph_7_data:
                sentence_new = f' -|->  {sentence}\n'
                print(sentence_new)
                product_total_text += sentence_new

        except Exception as e:
            pass

        if product_total_text == '':
            raise Exception('Product introduction is empty.')

        return product_total_text

    # get_order_from_product_json: Paragraph attribution and sorting based on feature grouping
    def get_order_from_product_json(self,feature_group_json):
        json_keys= feature_group_json.keys()
        order_list = []
        for i,v in enumerate(json_keys):

            for i in range(6):
                paragraph = f'self.dp.paragraph_{i + 1}()'
                group = eval(paragraph)

                if v == group[0]:
                    order_list.append(i+1)
                    break

        order_list = sorted(order_list)
        return order_list