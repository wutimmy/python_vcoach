r,c,h,w = input("").split(" ")
r = int(r)
c = int(c)
h = int(h)
w = int(w)

for i in range(1,(h+2)*r+1):
    s = ""
    if i == 1 or i == (h+2)*r+1:
        for j in range(c):  #w+c+1    
            if i == c-1:
                s = "|" + "-"*int(w) + "|" + "\n"
            else:
                s = "|" + "-"*int(w)
            print(s,end="")
    else:
        s = ""
        print(s)