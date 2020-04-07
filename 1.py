import re
from collections import Counter
from itertools import permutations

# r = "(hi|hello|hey)[ ]*([a-z]*)"
# print(re.match(r, "hey, what's up", flags=re.IGNORECASE))

r = r"[^a-z]*([y]o|[h']?ello|ok|hey|(good[ ])?(morn[gin']{0,3}|" \
    r"afternoon|even[gin']{0,3}))[\s,;:]{1,3}([a-z]{1,20})"

re_greeting = re.compile(r, flags=re.IGNORECASE)

# my_names = {'rosa', 'rose', 'chatty', 'chatbot', 'bot', 'chatterbot'}
# curt_names = {'hal', 'you', 'u'}
# greeter_name = 'Mohammad'
# match = re_greeting.match(input())
#
# if match:
#     at_name = match.groups()[-1]
#     if at_name in curt_names:
#         print("Good one.")
#     elif at_name.lower() in my_names:
#         print("Hi {}, How are you?".format(at_name))

print(Counter("Guten Morgen Rosa".split()))

print([" ".join(combo) for combo in \
       permutations("Good morning Rosa!".split(), 3)])
