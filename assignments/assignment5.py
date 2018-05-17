import random
import datetime
import hashlib

# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
rand1 = random.random()
# print(rand1)
rand2 = random.randrange(1, 11)
# print(rand2)
# rand3 = random.randint(1, 10)
# print(rand3)
print(rand1, rand2)


# 2) Use the datetime library together with the random number to generate a random, unique value.
now = datetime.datetime.now()
unique_value = "{}_{}".format(now, rand1)
print(unique_value)
unique_hash = hashlib.sha256(unique_value.encode()).hexdigest()
print(unique_hash)
