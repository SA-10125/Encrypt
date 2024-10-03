from pickle import*
op=open('crypt.dat','rb')
key,base,a='','',[]

while base=='':#cant take empty base.
    base=input("Enter the password: ")#trynna make it replicable based on a password that the user inputs.

for i in base:
    for j in range(ord(i)):
        key+=str((ord(i)*j)+(ord(i)*ord(i))+(j*j))
#print(key)#remove

try:#ive used append while encrypting, so ive to go through each element and take...
    while True:
        a=(load(op))#ive put it in as a list of numbers...
        ke,temp=0,0
        #print(a,'\n')#remove
        #see the actual file btw
        try:
            #decrypting
            ha=''
            key=key[::-1]#reversing the key cause (why not) thats what ive done in encrypting
            for i in a:#now decrypting that string 
                try:#restarting the key if key is traversed fully
                    ke=int(key[temp])
                except IndexError:
                    temp=0
                    ke=int(key[temp])
                temp+=1
                ha+=chr(i-ke)
            #print(ha,'\n')#remove
            key=key[::-1]#reversing again to get back original key
            d=open('store.dat','w',encoding='iso-8859-15')
            d.write(ha)
            d.close()
            d=open('store.dat','rb')
            ha=load(d)
            #print(ha,'\n')#remove
            out=''
            ke,temp=0,0
            for i in ha:
                try:#restarting the key if key is traversed fully
                    ke=int(key[temp])
                except IndexError:
                    temp=0
                    ke=int(key[temp])
                temp+=1
                out+=chr(i-ke)
            print(out)
            d.close()
            d=open('store.dat','w')#emptying store
            d.close()
        except ValueError:
            print("Wrong password entered.")
#just everything we did in encrypt in reverse and in reverse order of encryptions too.
except EOFError:
    op.close()
