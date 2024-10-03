from pickle import*
d=open('store.dat','wb')
key,base='',''

while base=='':#cant take empty base.
    base=input("Enter the password: ")#trynna make it replicable based on a password that the user inputs.

for i in base:#making the key
    for j in range(ord(i)):
        key+=str((ord(i)*j)+(ord(i)*ord(i))+(j*j))
#print(key)#remove

out=[]
ke,temp=0,0
l=input("Enter the string: ")

#encrypting
for i in l:
    try:#restarting the key if key is traversed fully
        ke=int(key[temp])
    except IndexError:
        temp=0
        ke=int(key[temp])
    temp+=1
    out.append(ord(i)+ke)
#print(out,'\n')#remove

dump(out,d)
d.close()

d=open('store.dat','r',encoding='iso-8859-15')
a=d.read()
#print(a,'\n')#remove
temp=0
ha=[]

key=key[::-1]#reversing the key cause why not
for i in a:#now encrypting that string
    try:#restarting the key if key is traversed fully
        ke=int(key[temp])
    except IndexError:
        temp=0
        ke=int(key[temp])
    temp+=1
    ha.append(ord(i)+ke)
d.close()

d=open('store.dat','w')#emptying store
d.close()

d=open('crypt.dat','ab')
#print(ha,'\n')#remove
dump(ha,d)
print("Saved.")
d.close()
#see the actual file btw
'''
what this does:

inputting:
    takes password which determines the key directly
    takes input string

encrypting:
    encrypts as list based on the key logic
    pickles and dumps that
    takes that pickled string from the file (raw, no unpickling)
    encypts that string based on the key logic (but key is reversed)
    pickles and dumps that encrypted string into file.

key logic mentioned here:
    traverses the string
    for each letter in the string (including space):
        ke=stores 1 number of the key (traverses key)
        take the ascii value using ord()
        then add that value by ke
        then append that in the list
        ke=next number in key (traversing)
'''
