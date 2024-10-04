from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
import os
from importlib import reload
import sys

os.environ["OPENAI_API_KEY"] = "YOUR API KEY"

examples = SimpleDirectoryReader(input_files=['data/train.csv']).load_data()
print("Loaded")

# define LLM
llm = OpenAI(model="gpt-4")
Settings.llm = llm

# build index and query engine
node_parser = SimpleNodeParser.from_defaults(chunk_size=260,chunk_overlap=2)
nodes = node_parser.get_nodes_from_documents(examples)
index = VectorStoreIndex(nodes)
writer = index.as_chat_engine()
try:
    import test
except:
    open('test.py', 'w')
    import test

def Test(sampleInputs, sampleOutputs):
    try:
        realOutputs = test.TestFunction(sampleInputs)
        print(realOutputs)
        if realOutputs == sampleOutputs:
            return False
        else:
            return ' With inputs ' + str(sampleInputs) + ' returned ' + str(realOutputs) + ', expected ' + str(sampleOutputs) + '. Rewrite the entire corrected script.'
    except Exception as ex:
        line_number = ex.__traceback__.tb_lineno
        try:
            return 'Line ' + str(line_number)+ ': ' + ex.message + ' Rewrite the entire corrected script.'
        
        except:
            return 'Line ' + str(line_number)+ ': ' + str(ex) + ' Rewrite the entire corrected script.'
    
#input = input('Write a function that:')
input = 'Write a python script that has one function called "TestFunction" which ' + ''
while True:
    print(input)
    output = writer.chat(input)
    print(output)
    code = str(output).split('```')[1][6:]
    with open('test.py', 'w') as file:
        file.write(code)
    reload(test)
    failed = Test('https://github.com/ollama/ollama', None)
    if failed:
        input = 'Error: ' + failed
    else:
        break