def string(str1, str2):
    list=[]
    n = 0
    n2 = 0
    for x in range(len(str1)):
        if str1[x]==str2[x]: 
            n = n + 1
        else:
            list.append(x)
            
    for x in list:
        for y in list:
            if str1[x]==str2[y]:
                n2 = n2 + 1
            else:
                continue
    print(n, n2)
    
string('abc', 'aab')