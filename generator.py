from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
import os
from importlib import reload
import translate
import sys

os.environ["OPENAI_API_KEY"] = "API KEY"

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

def GenerateExample():
    example = 'case\ninputs\nstr:volcano\nint:4\noutputs\nstr:volc\ncase\ninputs\nstr:word\nint:2\noutputs\nstr:wo'
    with open('example.txt', 'w') as file:
        file.write(example)

def ParseTest(filepath):
    inputs = []
    outputs = []
    with open(filepath, 'r') as file:
        phase = 'case'
        index = 0
        for line in file:
            line = line.rstrip()
            if phase == 'case':
                if line != 'case':
                    print('"'+line+'"')
                    raise Exception('Invalid test file format')
                inputs.append([])
                outputs.append([])
                phase = 'inputs'
                continue
            if phase == 'inputs':
                if line == 'inputs':
                    continue
                if line == 'outputs':
                    phase = line
                    continue
                var = line.split(':')[0]
                value = line.split(':')[1]
                if var == 'str':
                    inputs[index].append(value)
                elif var == 'int':
                    inputs[index].append(int(value))
                elif var == 'bool':
                    if value == 'True':
                        inputs[index].append(True)
                    elif value == 'False':
                        inputs[index].append(False)
                    else:
                        raise Exception('Invalid test file format')
                elif var == 'float':
                    inputs[index].append(float(value))
                elif var == 'char':
                    inputs[index].append(value[0])
            if phase == 'outputs':
                if line == 'case':
                    phase = 'inputs'
                    index += 1
                    inputs.append([])
                    outputs.append([])
                    continue
                var = line.split(':')[0]
                value = line.split(':')[1]
                if var == 'str':
                    outputs[index].append(value)
                elif var == 'int':
                    outputs[index].append(int(value))
                elif var == 'bool':
                    data = line.split(':')[1]
                    if data == 'True':
                        outputs[index].append(True)
                    elif data == 'False':
                        outputs[index].append(False)
                    else:
                        raise Exception('Invalid test file format')
                elif var == 'float':
                    outputs[index].append(float(value))
                elif var == 'char':
                    outputs[index].append(value[0])
    return (inputs, outputs)

inputs, outputs = ParseTest('example.txt')
print(inputs)
print(outputs)

ParseTest('example.txt')

def Test(values):
    testFunction = 'TestFunction('
    index = 0
    for value in inputs:
        testFunction += 'inputs[' + str(index) + '],'
        index += 1
    testFunction = testFunction[0:-1] + ')'
    firsthalf = 'from test import TestFunction\ndef Test(inputs):\n  print(inputs)\n  output = '
    secondhalf = '\n  return output'
    with open('translate.py', 'w') as translator:
        translator.write(firsthalf)
        translator.write(testFunction)
        translator.write(secondhalf)
    reload(translate)
    sampleInputs, sampleOutputs = values
    print(sampleInputs)
    try:
        realOutputs = translate.TestFunction(sampleInputs)
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
    
prompt1 = input('Write a function that, given (describe inputs): ')
prompt2 = input('returns (describe outputs): ')
prompt = 'Write a python script that has one function called "TestFunction" which given ' + prompt1 + ', returns ' + prompt2
test_cases = ''
#while True:
print(prompt)
output = writer.chat(prompt)
print(output)
code = str(output).split('```')[1][6:]
with open('test.py', 'w') as file:
    file.write(code)
if test_cases == '':
    test_cases = input('\nEnter name of test case file, or "help" to generate an example test file, or enter to skip test phase (not recommended unless testable inputs and outputs are not practical): ')
if test_cases == 'help':
    GenerateExample()
tests = ParseTest(test_cases)
for case in tests:
    failed = Test(case)
    if failed:
        prompt = 'Error: ' + failed