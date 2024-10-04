
def TestFunction(acceptable_inputs):
    while True:
        user_input = input("Please enter your input: ")
        if acceptable_inputs:
            if user_input in acceptable_inputs:
                return user_input
            else:
                print("Invalid input. Please try again.")
        else:
            try:
                return int(user_input)
            except ValueError:
                print("Invalid input. Please enter a number.")

# Test the function
print(TestFunction(['apple', 'banana', 'cherry']))
print(TestFunction([]))
