from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
import os
from assistant_functions import add, function

def get_input():
    while True:
        user_input = input('\nOptions:\n1. Generate a function\n2. Debug a script\n3. Add comments to script\n4. Add print statements to script for debugging purposes\n5. Revert last change to script\n6. Quit\n\nEnter number of desired option: ')
        if user_input in ['1', '2', '3', '4', '5', '6']:
            return user_input
        else:
            print("\nInvalid input. Please enter a number between 1 and 6.")

print('Loading model...')

os.environ["OPENAI_API_KEY"] = "API KEY"
examples = SimpleDirectoryReader(input_files=['data/train.csv']).load_data()

# define LLM
llm = OpenAI(model="gpt-4")
Settings.llm = llm

# build index and query engine
node_parser = SimpleNodeParser.from_defaults(chunk_size=260,chunk_overlap=2)
nodes = node_parser.get_nodes_from_documents(examples)
index = VectorStoreIndex(nodes)
writer = index.as_chat_engine()

while True:
    choice = get_input()
    if choice == '1':
        function.generate(writer)
    elif choice == '3':
        result = add.run(writer, False)
        if result:
            print(result)
    elif choice == '4':
        result = add.run(writer, True)
        if result:
            print(result)
    elif choice == '6':
        break