# Importing necessary functions from assistant_functions module
from assistant_functions import utils

# Function to run the script
def run(writer, debug):
    # If debug is True, set the prompt to ask for print statements
    if debug:
        prompt = 'Add print statements helpful for debugging to this script: '
    # If debug is False, set the prompt to ask for comments
    else:
        prompt = 'Add brief, sparse comments to this script: '
    
    # Get the name of the script from the user
    scriptname = input('\nEnter name of script to add to: ')
    
    # Open the script in read mode
    with open(scriptname, 'r') as script:
        # Read the original script
        original = script.read()
    
    # Create a backup of the original script
    utils.backup(scriptname, original)
    
    print('\nGenerating...')
    
    # Isolate the added comments or print statements
    added = utils.isolate(str(writer.chat(prompt + original)))
    
    # Open the script in write mode
    with open(scriptname, 'w') as script:
        # Write the added comments or print statements to the script
        script.write(added)
    
    # If there's an error, return 'Invalid script path'
    # except:
    #     return 'Invalid script path'