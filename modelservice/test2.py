from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from config import Config

class Ollama_test():
    def __init__(self,model = None):
        self.config = Config()

        if model is None:
            model = self.config.model_name()

        self.llm = Ollama(model=model)

    def ollama_langchain(self):
        result = self.llm.invoke("Tell me a joke")
        print(result)

    def ollama_langchain_stream(self):

        query = "Tell me a joke"
        for chunks in self.llm.stream(query):
            print(chunks)

    def ollama_prompt(self):
        template = """我真的很想去[location]旅行。我应该在那里做什么 """
        prompt = PromptTemplate(input_variables = ["location"],template=template)
        final_prompt = prompt.format(location="广东广州")
        print(f'最终提示词--{final_prompt}')
        # print(f'LLM输出--{self.llm.invoke(final_prompt)}')


if __name__ == '__main__':
    ollama = Ollama_test()
    # ollama.ollama_prompt()
    ollama.ollama_langchain()
    # ollama_langchain_stream()