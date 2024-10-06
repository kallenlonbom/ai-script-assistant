import re
import os
import sys
from assistant_functions import utils

def test():
    try:
        _original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        import test
        sys.stdout.close()
        sys.stdout = _original_stdout
    except Exception as ex:
        line_number = ex.__traceback__.tb_lineno
        try:
            return 'Error: Line ' + str(line_number)+ ': ' + ex.message + '. Rewrite the entire corrected script.'
        
        except:
            return 'Error: Line ' + str(line_number)+ ': ' + str(ex) + '. Rewrite the entire corrected script.'
        
def find_last_import(script):
    number = -1
    i = 0
    for line in script:
        if line.startswith('import') or line.startswith('from'):
            number = i
        i += 1
    return number

def insert(scriptname):
    imports = []
    code = []
    test = ''
    with open('assistant_functions/test.py', 'r') as function:
        ended = False
        for line in function:
            if ended:
                test += line
            else:
                if line.startswith('import') or line.startswith('from'):
                    imports.append(line)
                elif line.startswith('# Test'):
                    ended = True
                else:
                    code.append(line)
    with open(scriptname, 'r+') as script:
        original = script.readlines()
        script.seek(0, 0)
        newImports = 0
        for line in imports:
            if line not in original:
                script.write(line)
                newImports += 1
        i = 0
        end_imports = find_last_import(original)
        for line in original:
            if i > end_imports + newImports:
                for codeline in code:
                    script.write(codeline)
                end_imports = 10000000
            script.write(line)
            i += 1
    with open('assistant_functions/backups/' + scriptname.split('/')[-1], 'w') as backup:
        for line in original:
            backup.write(line)

    return re.sub(r'print\((.*?)\)', r'\1', test)

def generate(writer):
    prompt = 'Write a python script that has one function which ' + input('Write a function that: ') + '. Test it on ' + input('Test it on: (leave blank to auto generate test)') 
    print('\nGenerating...\n')
    while True:
        output = writer.chat(prompt)
        code = utils.isolate(output)
        with open('assistant_functions/test.py', 'w') as file:
            file.write(code)
        failed = test()
        if failed:
            prompt = failed
        else:
            scriptname = input('Enter name of script to insert function into: ')
            usage = insert(scriptname)
            print('\nFunction and requisite imports added to ' + scriptname + '\n\nUsage example:\n\n' + usage)
            break