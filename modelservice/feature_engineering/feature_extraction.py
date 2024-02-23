from modelservice.model.model import LLM_Model
from modelservice.common.utils import Common_Utils

class Feature_Engineering(LLM_Model):
    def __init__(self):
        super().__init__()
        self.cu =Common_Utils()

    def extraction(self,sentence):
        feature_string = self.ollama_json(sentence=sentence)
        feature_json = self.cu.string_2_json(json_string=feature_string)
        print(feature_json)
        return feature_json



if __name__ == '__main__':
    from modelservice.database.dataset import Dateset

    sentence = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."

    ds = Dateset()
    ds.make_dataset()

    fe = Feature_Engineering()
    result = fe.extraction(sentence=sentence)
