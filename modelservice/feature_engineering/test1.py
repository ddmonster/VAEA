from transformers import pipeline

sentences ="I'd like to buy a red fryer that has 2000 watts max."


ner = pipeline("ner", grouped_entities=True)
results = ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")
print(results)

pipe = pipeline("token-classification", model="rowdy-store/products-ner")
print(pipe(sentences))




question_answerer = pipeline("question-answering")
answer = question_answerer(
    question="Extracting numbers",
    context="2000 watts")
print(answer)

a = [{'entity': 'B-PRODUCT_CHARACTERISTICS', 'score': 0.9417403, 'index': 8, 'word': 'red', 'start': 18, 'end': 21},
     {'entity': 'B-PRODUCT_TYPE', 'score': 0.43929175, 'index': 9, 'word': 'fry', 'start': 22, 'end': 25},
     {'entity': 'I-PRODUCT_TYPE', 'score': 0.64371413, 'index': 10, 'word': '##er', 'start': 25, 'end': 27},
     {'entity': 'B-PRODUCT_CHARACTERISTICS', 'score': 0.40628746, 'index': 13, 'word': '2000', 'start': 37, 'end': 41},
     {'entity': 'I-PRODUCT_CHARACTERISTICS', 'score': 0.6798968, 'index': 14, 'word': 'watts', 'start': 42, 'end': 47},
     {'entity': 'I-PRODUCT_CHARACTERISTICS', 'score': 0.6063433, 'index': 15, 'word': 'max', 'start': 48, 'end': 51}]
b = {'score': 0.5718945264816284, 'start': 16, 'end': 27, 'answer': 'a red fryer'}

summarizer = pipeline("summarization")
results = summarizer(
    """
   ["Auto ignites feature for spark in LPG gas deep fryer commercial", "Stainless Steel LPG Gas Deep Fryer for Home and commercial uses", "4 Year warranty on burner only", "This Commercial Gas Deep Fryer is made up of Stainless Steel Material and comes in Silver colour with 6 L capacity.", "Light weight Body gas commercial fryer", "Steel Plate Construction Body gas deep fryer commercial", "Inclusions- Burner , Steel Tank , Mesh with Handle, Top Lid / cover , Wire is included in the machine.", "CAN BE USE ONLY BY LPG GAS NOT BY ELECTRICTY"]
    """
)
print(results)


# from transformers import AutoTokenizer
#
# tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
# example = "My name is Sylvain and I work at Hugging Face in Brooklyn."
# encoding = tokenizer(example)
# print(encoding.tokens())

generator = pipeline("text-generation")
a= generator("In this course, we will teach you how to")
print(a)