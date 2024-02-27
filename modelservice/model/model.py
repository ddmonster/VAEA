from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory,ConversationBufferMemory,ConversationBufferWindowMemory,ConversationSummaryBufferMemory

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from modelservice.common.config import Config



class LLM_Model():
    def __init__(self, model=None):
        self.config = Config()

        if model is None:
            model = self.config.model_name()

        self.llm = Ollama(model=model)

    def ollama_extraction_feature(self,sentence):

        response_schemas = [
            ResponseSchema(name="product_name", description=self.config.prompt_info()["product_name"]),
            ResponseSchema(name="brand", description=self.config.prompt_info()["brand"]),
            ResponseSchema(name="capacity",description=f"{self.config.prompt_info()['capacity']} Please fill in Arabic numerals."),
            ResponseSchema(name="colour", description=self.config.prompt_info()["colour"]),
            ResponseSchema(name="number_of_reviews", description=self.config.prompt_info()["number_of_reviews"]),
            ResponseSchema(name="wattage",description=f"{self.config.prompt_info()['wattage']} Please fill in Arabic numerals."),
            ResponseSchema(name="sale_price",description=f"{self.config.prompt_info()['sale_price']} Please fill in Arabic numerals."),
            ResponseSchema(name="country_of_origin", description=self.config.prompt_info()["country_of_origin"]),
            ResponseSchema(name="home_kitchen_rank",description=f"{self.config.prompt_info()['home_kitchen_rank']} Please fill in Arabic numerals."),
            ResponseSchema(name="air_fryers_rank",description=f"{self.config.prompt_info()['air_fryers_rank']} Please fill in Arabic numerals."),
            ResponseSchema(name="Weight",description=f"{self.config.prompt_info()['Weight']} Please fill in Arabic numerals."),
            ResponseSchema(name="Has_Nonstick_Coating", description=f"{self.config.prompt_info()['Has_Nonstick_Coating']} Please fill in Yes or No"),
            ResponseSchema(name="Material", description=self.config.prompt_info()['Material']),
            ResponseSchema(name="Control_Method", description=self.config.prompt_info()["Control_Method"]),
            ResponseSchema(name="Recommended_Uses_For_Product",description=self.config.prompt_info()["Recommended_Uses_For_Product"]),
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

    def ollama_generation_one_paragraph(self,response_schemas,product_name,paragraph_intro,input_json,word_num=50):
        oup_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = oup_parser.get_format_instructions()

        template = """
                  You are a professional product introduction [product_name] that will generate a text introducing a fryer product based on json data entered by the user. [paragraph_intro] This paragraph should be attractive and relevant to the user. In addition, the paragraph should be limited to about [word_num] words. Only results are needed, no need to generate redundant summaries and any emoji.

                  {format_instructions}

                  %user input：
                  {user_input}

                  your output：
                  """
        template = template.replace("[product_name]",product_name)
        template = template.replace("[paragraph_intro]", paragraph_intro)
        template = template.replace("[word_num]", str(word_num))

        prompt = PromptTemplate(input_variables=["user_input"], template=template,
                                partial_variables={"format_instructions": format_instructions})
        promptValue = prompt.format(user_input=f"{input_json}")

        result = self.llm(promptValue)

        return result



if __name__ == '__main__':

    # ollama.ollama_summary_split()
    # ollama.ollama_summary()
    import re, json

    ollama = LLM_Model()
    # ollama.memory_chain()

    # ollama.ollama_chain()
    # ollama.ollama_prompt2()
    # ollama.ollama_prompt1('广东深圳')
    # ollama.ollama_langchain()
    # ollama_langchain_stream()