def isolate(output):
    segments = str(output).split('```')
    if segments.__len__() > 1:
        return segments[1][6:]
    else:
        return segments[0]

def backup(scriptname, original):
    with open('assistant_functions/backups/' + scriptname.split('/')[-1], 'w') as backup:
        backup.write(original)