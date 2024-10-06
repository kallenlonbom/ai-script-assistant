def isolate(output):
    return str(output).split('```')[1][6:]

def backup(scriptname, original):
    with open('assistant_functions/backups/' + scriptname.split('/')[-1], 'w') as backup:
        backup.write(original)