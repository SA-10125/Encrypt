from pickle import*
d=open('crypt.dat','wb')
key='726728734034610974319472038472305624087634983598275982395823948274092384283275874568437561094845394856837468134817264837698129482395874957237230985095734085734857084164816514861846513514681687461645106413110846512365132651239638527411479841000008416846784'
out=[]
ke,temp=0,0

l=input("Enter the string: ")

#encrypting
for i in l:
    ke=int(key[temp])
    temp+=1
    out.append(ord(i)+ke)
print(out,'\n')#remove
dump(out,d)
d.close()
d=open('crypt.dat','r')
a=d.read()
print(a,'\n')#remove
temp=0
ha=[]
for i in a:
    ke=int(key[temp])
    temp+=1
    ha.append(ord(i)+ke)
d.close()
d=open('crypt.dat','wb')
print(ha,'\n')#remove
dump(ha,d)
d.close()

#see the actual file.
d=open('crypt.dat','r')
a=d.read()
print(a,'\n')#remove
d.close()

#decrytping
d=open('crypt.dat','rb')
a=load(d)
ha=''
temp=0
for i in a:
    ke=int(key[temp])
    temp+=1
    ha+=chr(i-ke)
d.close()
d=open('crypt.dat','w')
d.write(ha)
d.close()
d=open('crypt.dat','rb')
out=load(d)
d.close()
wow=''
temp=0
for i in out:
    ke=int(key[temp])
    temp+=1
    wow+=chr(i-ke)
print(wow)

