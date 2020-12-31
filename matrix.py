#made with following function:
i = 0
for y in range(14, -1, -1):
    for x in range (0,20):
        if(y%2 == 0):
            print(str(20*y+x) + ', ', end='\n' if (x == 19) else ' ')
        else:
            print(str(20*(y+1) - x - 1) + ', ', end='\n' if (x == 19) else ' ')
        i+=1


