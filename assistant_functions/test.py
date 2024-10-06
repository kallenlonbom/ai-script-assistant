
def lowercase_first_letter(s):
    if not s:
        return s
    else:
        return s[0].lower() + s[1:]

# Test the function
print(lowercase_first_letter("Hello"))
print(lowercase_first_letter("WORLD"))
print(lowercase_first_letter("Python"))
