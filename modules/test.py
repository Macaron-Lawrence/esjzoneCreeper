import json
from modules.EPUBbuilder import EPUBgenerator

B = {};

with open('./output/test.json','r',encoding='utf-8') as f1:
    B = json.load(f1)

EPUBgenerator(B)