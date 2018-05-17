""" List """
simple_list = [1, 2, 3, 4]
simple_list.extend([5, 6, 7])
print(simple_list)
# del(simple_list[0])
del simple_list[-1]
print(simple_list)

""" Dictionary """
d = {'name': 'Rick'}
print(d.items())
del d['name']
print(d)

for k, v in d.items():
    print(k, v)

""" Tuple """
t = (1, 2, 3)
print(t.index(2))   # 1
# print(t.index(4))   # Error
# del t[0]    # Error, because tuples are immutable!s


""" Set """
s = {'Rick', 'Jack', 'Dino', 'Rick'}
print(s)
# del s['Rick']   # Erorr, use discard
s.discard('Rick')
print(s)