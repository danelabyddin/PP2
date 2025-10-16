import re

text = "Hello there From PrinProg Lab"
result = re.findall(r'[A-Z][a-z]+', text)
print(result)
