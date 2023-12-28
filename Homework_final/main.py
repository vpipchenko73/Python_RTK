
a= [{'author': 2, 'author__username': 'Umba'}, {'author': 2, 'author__username': 'Umba'}, {'author': 2, 'author__username': 'Umba'},
    {'author': 4, 'author__username': 'sun'}, {'author': 4, 'author__username': 'sun'}, {'author': 4, 'author__username': 'sun'},
    {'author': 6, 'author__username': 'admin'}]
b = {'author': 2, 'author__username': 'Umba'}

print (b in a)

out = []

print (a)
for i in a:
    if (i in out) == False:
        out.append(i)

print (out)
