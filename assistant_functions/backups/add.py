from assistant_functions import utils

def run(writer, debug):
    if debug:
        prompt = 'Add print statements helpful for debugging to this script: '
    else:
        prompt = 'Add brief, sparse comments to this script: '
    # try:
    scriptname = input('\nEnter name of script to add to: ')
    with open(scriptname, 'r') as script:
        original = script.read()
    utils.backup(scriptname, original)
    print('\nGenerating...')
    added = utils.isolate(str(writer.chat(prompt + original)))
    with open(scriptname, 'w') as script:
        script.write(added)
    # except:
    #     return 'Invalid script path'