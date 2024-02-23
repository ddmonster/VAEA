from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain



from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from modelservice.common.config import Config


class LLM_Model():
    def __init__(self, model=None):
        self.config = Config()

        if model is None:
            model = self.config.model_name()

        self.llm = Ollama(model=model)

    def ollama_json(self,sentence):
        response_schemas = [
            ResponseSchema(name="product_name", description="This is the name of the product"),
            ResponseSchema(name="brand", description="This is the brand of the product"),
            ResponseSchema(name="capacity",description="This is the capacity of the product. Please fill in Arabic numerals."),
            ResponseSchema(name="colour", description="This is the colour of the product"),
            ResponseSchema(name="number_of_reviews", description="This is the number of reviews of the product"),
            ResponseSchema(name="wattage",description="This is the power wastage of the product. Please fill in Arabic numerals."),
            ResponseSchema(name="sale_price",description="This is the sale price of the product. Please fill in Arabic numerals."),
            ResponseSchema(name="country_of_origin", description="This is the origin country of the product."),
            ResponseSchema(name="home_kitchen_rank",description="This is the rank of the product in the home kitchen rank. Please fill in Arabic numerals."),
            ResponseSchema(name="air_fryers_rank",description="This is the rank of the product in the air fryers rank. Please fill in Arabic numerals."),
            ResponseSchema(name="Weight",description="This is the Weight of the product. Please fill in Arabic numerals."),
            ResponseSchema(name="Has_Nonstick_Coating", description="This is whether the product contains a non-stick coating. Please fill in Yes or No"),
            ResponseSchema(name="Material", description="This is the material of the product"),
            ResponseSchema(name="Control_Method", description="This is the control method of the product"),
            ResponseSchema(name="Recommended_Uses_For_Product",description="This is the use of the product which is what users can do with this item"),


        ]
        oup_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = oup_parser.get_format_instructions()

        template = """
           You are a professional product introduction bot that will extract product information from the user's input and fill in the json corresponding key-value pairs. If you don't find a feature that matches a key in the json from the user's input, then the value in this key should be null.

           {format_instructions}

           %user input：
           {user_input}

           your output：
           """
        prompt = PromptTemplate(input_variables=["user_input"], template=template,
                                partial_variables={"format_instructions": format_instructions})
        promptValue = prompt.format(
            user_input=sentence)

        result = self.llm(promptValue)

        return result



if __name__ == '__main__':

    # ollama.ollama_summary_split()
    # ollama.ollama_summary()
    import re, json

    ollama = LLM_Model()
    result = ollama.ollama_json()
    print(result)
    # 使用正则表达式匹配JSON数据
    pattern = r'\{.*\}'
    match = re.search(pattern, result, re.DOTALL)
    if match:
        json_data = match.group()
        try:
            json_data = json.loads(json_data)
            print(json_data)  # 打印格式化后的JSON数据
        except json.JSONDecodeError as e:
            Exception(f"Error decoding JSON: {e}")
    else:
        print("No JSON data found.")

    # ollama.ollama_chain()
    # ollama.ollama_prompt2()
    # ollama.ollama_prompt1('广东深圳')
    # ollama.ollama_langchain()
    # ollama_langchain_stream()