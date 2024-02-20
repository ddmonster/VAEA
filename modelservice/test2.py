from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

from langchain.agents import load_agent
from  langchain.agents import initialize_agent
import json

# from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OllamaEmbeddings
# from langchain.prompts import FewShotPromptTemplate,PromptTemplate

from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from langchain.prompts import ChatPromptTemplate,HumanMessagePromptTemplate
from config import Config

class Ollama_test():
    def __init__(self,model = None):
        self.config = Config()

        if model is None:
            model = self.config.model_name()

        self.llm = Ollama(model=model)

    def ollama_langchain(self,sentence):
        result = self.llm.invoke(sentence)
        print(result)

    def ollama_langchain_stream(self,sentence):

        for chunks in self.llm.stream(sentence):
            print(chunks)

    def ollama_prompt1(self,location):
        template = """我真的很想去{location}旅行。我应该在那里做什么 """
        prompt = PromptTemplate(input_variables = ["location"],template=template)
        final_prompt = prompt.format(location=location)
        print(f'最终提示词--{final_prompt}')
        output= self.ollama_langchain(final_prompt)

        print(f'LLM输出--{output}')

    # def ollama_prompt2(self):
    #     examples = [{"input":"海盗","output":"船"},{"input":"飞行员","output":"飞机"},
    #                 {"input":"驾驶员","output":"汽车"},{"input":"树","output":"地面"},
    #                 {"input":"鸟","output":"鸟巢"}]
    #
    #     template = """示例输入：{input} \n 示例输出： {output}"""
    #     example_prompt = PromptTemplate(input_variables = ["input", 'output'],template=template)
    #
    #     #根据予以选择与您的输入相似的示例
    #     example_selector = SemanticSimilarityExampleSelector.from_examples(examples,
    #                                                                        #用于测量语义相似性的嵌入类
    #                                                                        OllamaEmbeddings(),FAISS,
    #                                                                        k=2)
        #
        # similar_prompt = FewShotPromptTemplate(
        #     example_selector =example_selector,
        #     example_prompt=example_prompt,
        #     prefix = '根据下面示例，写出输出',
        #     suffix = '输入：{noun} \n输出：',
        #     input_variables = ["noun"]
        # )
        # my_noun='学生'
        # print(similar_prompt.format(noun=my_noun))

        # final_prompt = prompt.format()
        # print(f'最终提示词--{final_prompt}')
        # output= self.ollama_langchain(final_prompt)
        #
        # print(f'LLM输出--{output}')

    #格式化输出
    def ollama_json(self):
        response_schemas = [
            ResponseSchema(name="bad_string",description="这是一个格式不正确的用户输入字符串"),
            ResponseSchema(name="good_string",description="这是您的回复，重新格式化的回复")
        ]
        oup_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = oup_parser.get_format_instructions()

        template = """
        您将从用户那里得到一个格式不正确的字符串。重新格式化并确保所有单词拼写正确
        
        {format_instructions}
        
        %用户输入：
        {user_input}
        
        你的响应：
        """
        prompt = PromptTemplate(input_variables = ["user_input"],template=template,partial_variables={"format_instructions":format_instructions})
        promptValue=prompt.format(user_input='欢迎广州来到')
        print(promptValue)
        print(self.llm(promptValue))

    def ollama_chain(self):
        #第一个任务
        template = """
        您的工作是根据用户建议的区域制作一道经典菜谱。
        %用户位置
        {user_location}
        
        AI回答：
        """
        prompt_template = PromptTemplate(input_variables = ["user_location"],template=template)
        location_chain=LLMChain(llm=self.llm,prompt=prompt_template)

        #第二个任务
        template = """
        给出一个简短的食谱，说明如何在家做这道菜
        %菜谱
        {user_meal}
        
        AI回答
        """
        prompt_template = PromptTemplate(input_variables = ["user_meal"],template=template)
        meal_chain=LLMChain(llm=self.llm,prompt=prompt_template)


        #两个任务连在一起
        overall_chain=SimpleSequentialChain(chains=[location_chain,meal_chain],verbose=True)
        review = overall_chain.run('广东广州')
        print(review)

    def ollama_agent(self):
        pass

    #总结文本
    def ollama_summary(self):
        template="""
        %指示：
        请总结下面的一段文字，以5岁儿童都能理解的方式回答
        
        %文本
        {text}
        """
        prompt = PromptTemplate(input_variables = ["text"],template=template)
        confuxing_text ="""
        LangChain 是一个应用框架，旨在简化使用大型语言模型的应用程序。作为一个语言模型集成框架，LangChain 的用例与一般语言模型的用例有很大的重叠。 重叠范围包括文档分析和总结摘要, 代码分析和聊天机器人。LangChain提供了一个标准接口，用于将不同的语言模型（LLM）连接在一起，以及与其他工具和数据源的集成。LangChain还为常见应用程序提供端到端链，如聊天机器人、文档分析和代码生成。 LangChain是由Harrison Chase于2022年10月推出的开源软件项目。它已成为LLM开发中最受欢迎的框架之一。LangChain支持Python和JavaScript语言，并与各种LLM一起使用，如GPT-4、BERT和T5。
        """
        print("---------Prompt Begin---------")
        final_prompt = prompt.format(text=confuxing_text)
        print(final_prompt)
        print("---------Prompt End---------")
        output=self.llm(final_prompt)
        print(output)


    #分段总结
    def ollama_summary_split(self):
        text="""
        1495年2月，当时的阿伯丁主教威廉·艾尔芬斯通受苏格兰国王詹姆士四世差遣，到罗马求见教皇亚历山大六世，希望教皇御许于阿伯丁老城区（Old Aberdeen）成立一所大学，称国王学院（King's College）。教皇在1495年2月6日与艾尔芬斯会面，在细细询问过为何要于阿伯丁成立大学、以及财政方面如何维持之后，覆以教皇训令（Papal Bull），阿伯丁大学正式成立。
作为一所公立的综合大学，阿伯丁大学的理学、工程、医学、法学、管理学等都享有良好的声誉。法学院是英国最好的法学院之一；医学院则是英国第一所医学院；商学院拥有AACSB、ACCA、CMI等国际认证，有着国际性的声誉；工商管理专业全英第3 [3]；石油类专业全球第2 [4]。其它如海洋工程、通讯、电子、教育等专业也有着非常强的实力。
英国前首相丘吉尔、前任港督卫亦信等均担任过阿伯丁大学的名誉校长，现任校长是查尔斯王子的夫人、英国王妃卡米拉殿下（罗撒西公爵夫人），她于2013年起担任这一职位。
1497年，大学设立了世界上第一个讲英语的医学教学职位，同时成立了英语系国家第一所医学院。大学主要为苏格兰北部培养医生、教师和牧师，并为当时的苏格兰政府培养律师和管理人才。1593年，第五代马修伯爵乔治·基斯在南面阿伯丁的新城区中心地区创立了阿伯丁第二所大学马修学院（Marischal College）。
1860年，两所学院根据英国议会通过的“1858年苏格兰大学法案”（Universities (Scotland) Act 1858）合并，正式称为阿伯丁大学。法案还同时规定大学的校龄从国王学院起算，因而是苏格兰第三和英国第五老的大学。之前的四所大学按建校时间先后顺序分别是牛津大学、剑桥大学、圣安德鲁斯大学和格拉斯哥大学
    合并后的国王学院校址主要教授人文艺术和神学，而马修学院所在地主要教授医学和法律。1892年，新的科学院在马修学院内建立。1894年，大学第一批女学生入学。1950年，大学大量增加招生，马修学院由于地处阿伯丁市中心，逐渐无法容纳越来越多的师生。除医科外，大学的主要授课地点逐渐往北面的国王学院原址迁移。马修学院主要只作为艺术博物馆和学生毕业的大礼堂之用，而其古老优美的建筑风格也是阿伯丁市中心的旅游景点之一。
2001年阿伯丁区的北部教育学院合并，教育系于同年成立。在2003年大学做出内部重组，之前五个学系重组成三个学院。学院内的小学院，如商学院等亦于同年成立。
2006年，在2月大学与阿伯丁市地区政府达成协议，将马修学院租给阿伯丁市地区政府作为办公室使用，年期为175年。大学作出一连串大规模投资，为未来作出准备。大学在未来十年将会使用2.3亿英镑来提升学校的设备。投资项目包括医学大楼，图书馆，体育中心等等。大学更成立了一系列的“第六世纪奖学金”并在各科增聘了多位教授。
阿伯丁大学位于风景怡人的苏格兰东海岸第三大城市阿伯丁市，又名花岗石城，七十年代起，阿伯丁迅速发展成为开发英国北海油田的最大基地，负责开采的许多大型石油公司都是以阿伯丁作为转运母港与总部所在地，因此该城又有“欧洲的石油首都”之称。学校500年历史的古建筑群仍在使用当中，并早已成为苏格兰的风景名胜。
2021年3月，发起成立英国卓越专业大学联盟。
大学分六个学院：人文艺术学院（Faculty of Arts）、科学学院（Faculty of Science）、工程学院（Faculty of Engineering）、医学与牙医学院（Faculty of Medicine and Dentistry）、商学院（Business School）、社会科学与法律学院（Faculty of Social Sciences and Law）。
提供涵盖文学、生物、物理、地质科学、地理、古典学（古代史为主）、历史研究、牙医学、戏剧、经济、会计与金融、管理、历史、语言、法律、医药、政治、社会学、公共政策、社会政策及兽医学等领域的120多个学士学位课程，100多门授课式硕士和研究生文凭课程以及传统的博士研究项目。学校的航空航天工程、电子工程、医学、地球大气工程、地质学、法律、经济学、教育学、政治学、会计与金融学、媒体艺术等课程都达到世界一流的水准。
        """
        num_tokens=self.llm.get_num_tokens(text)
        print(num_tokens)
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n","\n"],chunk_size=1000,chunk_overlap=200)
        docs = text_splitter.create_documents([text])
        print(f"You now have {len(docs)} docs ")

        #调用链
        chain =load_summarize_chain(llm=self.llm,chain_type="map_reduce",verbose=True) #verbose True可以查看发送给LLM的内容
        output = chain.run(docs)
        print(output)

if __name__ == '__main__':
    ollama = Ollama_test()
    # ollama.ollama_summary_split()
    # ollama.ollama_summary()
    ollama.ollama_json()
    # ollama.ollama_chain()
    # ollama.ollama_prompt2()
    # ollama.ollama_prompt1('广东深圳')
    # ollama.ollama_langchain()
    # ollama_langchain_stream()