'''
the idea is to do something like tor...
first, we take a username and password
then we create a file name and location using that username and password - location 1
we have 3 keys in total including the password
we ask the user to answer 2 recovery questions and remember their answer should they need to recover their account.
then, we make a key each from the password - key 1, and each recovery question, key 2 and 3.
in location 1, we encrypt and store key 2 using key 1. location of key 3 is determined by key 2 and the username.
this way, key 1 cannot directly acces key 3, it can only acces key 2. i.e the username and password (key 1) that you enter (after signup) can only open the location and decrypt key 2.
on decrypting key 2, we get the location of key 3 which is encrypted based on key 2 and stored. this key decrypts the contents. the name of the contents is the username.
and its location is the same normal place.
this way, only key 3 can acces the contents. its a very simple thing. but if someone copies the contents file (say, onto a pendrive/different system), they cant read the contents
simply because the contents are not encrypted based on the username or the password.
the contents are encrypted based on key 3 (which is determined by the second recovery question and encrypted by key 2 (which is determined by the first recovery question and encrypted by the password))
do you see the onion?
now you may ask, well, they can just copy the content file, key 2 file and key 3 file and transfer that right?, thats the catch. they do not know the location of key 2 or 3.
remember, the location of those are determined by the password and the key 2 in conjunction with the username respectively.
this way, the username and password can only acces and decrypt key 2. key 2 can only acces and decrypt key 3 and key 3 can only access and decrypt the contents.
this way, if any of the three keys are missing, the file cannot be read.
and these files are not conveniently stored. their locations are determined by each other.
now yes, the person can get the username and password and using that find the location of, and decrypt key 2 and using that, find the location of and decrypt key 3, and using that, decrypt the contents,
but at that point, you might as well just ask the user for his recovery questions also.
if needed, we can create more levels like storing location 1 which is determined by key 3 in a different location 0 which is determined by the username etc...
(we could theoretically even automate this whole process and create n number of keys...)

ok, so it turns out, its hard to create a random file location and save it so im saving it all in *C:\logs\storage python code*. will see if i can make it random later...
the problem is that each computer has different files and i dont have acces to the names/directories of all those so...
but its fine, the names of the files are different even though its in the same place and its just random to the naked eye so no one can find the key anyway...

IMP fix ASAP.
If any answer/pwd is the same as someone elses, then it overwrites that file. This creates problems. Think. (Maybe we can make the question very subjective. (This does not inherently solve the problem tho.)
IMP problem. I still want each to be indipendent of each other and of the usn and pwd tho. but if we can make it random but using seed, we may be able to hold the anonymity while still relating it in a way that
you couldnt trace back. just the Ls i mean. we could make it dependent on the usn and/or pwd too but using random.seed(). That way, each is unique and at the same time, having the L, you cant tell the usn.
if we need it to be indipendent of each other such that we can just send 1 file to servers like in tor (in the vid by computerphile), we can just send the part which is needed for the
 for i in usn:
        j=ord(i)
        if len(L2)<200:
            rn.seed(j)
            L2+=str(rn.randint(0,10000))
at the end of the file/key.


P.S - If you want to see the stored data, change .dat to .txt everywhere in the code. then you can open the files where the data is stored and read them, there is no problem.
IMP --> If your computer does not have a C:\\logs, you can just change that location (at every instance in the source code) to wherever you need the keys to be stored...
        I recommend putting it somewhere no one will care to see or somewhere packed and full of junk/random files.
        (cause then no one hacking will find the key) (but also somewhere that is common in all systems in case you share it to someone or something)
IMP --> Note: The folder must still be editable. i.e: you must be allowed and able to create and store (.dat) files on there...

The code works fine for upto 10,000 characters to be stored.
'''

def encrypt(key,AD,contents):
    import pickle
    #encrypt key logic

    #fill list...
    out=[]
    ke,tempo=0,0
    a=int(key[1])
    for i in contents:
        out.append(ord(i))
    

    for i in range(a):
        for j in range(len(out)):
            try:#restarting the key if key is traversed fully
                ke=int(key[tempo])
            except IndexError:
                tempo=0
                ke=int(key[tempo])
            tempo+=1
            if i%2==0:
                out[j]=out[j]+ke
            else:
                out[j]=out[j]-ke


    #pickling
    d=open('store.dat','wb')
    pickle.dump(out,d)
    d.close()


    #encrypting that pickled content using key logic
    key=key[::-1]#reversing the key cause why not


    d=open('store.dat','r',encoding='iso-8859-15')
    con=d.read()


    out=[]
    ke,tempo=0,0
    a=int(key[1])

    for i in con:
        out.append(ord(i))
        
    for i in range(a):
        for j in range(len(out)):
            try:#restarting the key if key is traversed fully
                ke=int(key[tempo])
            except IndexError:
                tempo=0
                ke=int(key[tempo])
            tempo+=1
            if i%2==0:
                out[j]=out[j]+ke
            else:
                out[j]=out[j]-ke
    d.close()
    key=key[::-1]#reversing the key back to normal
    #deleting store
    import os
    os.remove('store.dat')
    #putting the encrypted contents in the file.
    d=open(f'{AD}.dat','wb')
    pickle.dump(out,d)
    d.close()


def decrypt(key,AD):
    import pickle
    try:
        d=open(f'{AD}.dat','rb')
    except FileNotFoundError:
        print("Incorrect Username or Password.")
        exit()
    out=pickle.load(d)
    d.close()
    ke,tempo=0,0
    key=key[::-1]#reversing the key
    a=int(key[1])
    for i in range(a):
        for j in range(len(out)):
            try:#restarting the key if key is traversed fully
                ke=int(key[tempo])
            except IndexError:
                tempo=0
                ke=int(key[tempo])
            tempo+=1
            if i%2==0:
                out[j]=out[j]-ke
            else:
                out[j]=out[j]+ke
    data=''
    for i in out:
        data+=str(chr(i))
    key=key[::-1]#reversing the key back to normal
    d=open('store.dat','w',encoding='iso-8859-15')
    d.write(data)
    d.close()
    d=open('store.dat','rb')
    out=pickle.load(d)
    d.close()
    ke,tempo=0,0
    a=int(key[1])
    for i in range(a):
        for j in range(len(out)):
            try:#restarting the key if key is traversed fully
                ke=int(key[tempo])
            except IndexError:
                tempo=0
                ke=int(key[tempo])
            tempo+=1
            if i%2==0:
                out[j]=out[j]-ke
            else:
                out[j]=out[j]+ke
    content=''
    for i in out:
        content+=str(chr(i))
    #deleting store
    import os
    os.remove('store.dat')
    return(content)

    
def signup():#first time, we're creating everything
    import random as rn
    contents,key1,key2,key3,usn,pwd,L1,L2='','','','','','','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\'
    print("If this is your first time running this code, got to this directory *C:\\logs* and create a file called *storage python code* if it does not exist")
    #with enough users entered, no one can und it dw (names are random)
    temp=1
    while usn=='' or temp==1:
        usn=input("Enter your username: ")
        try:
            d=open(f'{usn}.dat','rb')
            print('Username aldready taken.')
            d.close()
        except FileNotFoundError:
            temp=0
    while pwd=='' or len(pwd)<8:
        pwd=input("Enter your password (more than 8 characters): ")
    while contents=='':
        contents=input("Enter the contents to be entered: ")
    
    for i in pwd:#making key 1
        for j in range(ord(i)*2):
            rn.seed(j)
            t=str(rn.randint(0,1000))
            key1+=t
    rn.seed(ord(key1[0])+int(key1[-1]))
    t=rn.randint(0,len(key1)//2)
    key1=key1[t::]
    if len(key1)>2000:
        key1=key1[0:2000]
    
    #making L1 (name), stores key 2
    for i in usn:
        j=ord(i)
        if len(L1)<100:
            rn.seed(j)
            L1+=str(rn.randint(0,10000))
    for i in key1:
        if len(L1)<200:
             rn.seed(i)
             L1+=str(rn.randint(0,10000))

    q1,q2='',''
    while q1=='' or len(q1)<8:
        q1=input("Enter the name of your first school (more than 8 characters): ")#can be any question
    while q2=='' or len(q2)<8:
        q2=input("Enter your first nickname (more than 8 characters): ")#can be any question

    for i in q1:#making key 2
        for j in range(ord(i)*2):
            rn.seed(j)
            t=str(rn.randint(0,1000))
            key2+=t
    rn.seed(ord(key2[0])+int(key2[-1]))
    t=rn.randint(0,len(key2)//2)
    key2=key2[t::]
    if len(key2)>2000:
        key2=key2[0:2000]

    for i in q2:#making key 3
        for j in range(ord(i)*2):
            rn.seed(j)
            t=str(rn.randint(0,1000))
            key3+=t
    rn.seed(ord(key3[0])+int(key3[-1]))
    t=rn.randint(0,len(key3)//2)
    key3=key3[t::]
    if len(key3)>2000:
        key3=key3[0:2000]
        
    #making L2 (name), stores key 3
    L2+=key2[-1]
    for i in key2:
        if len(L2)<100:
             rn.seed(i)
             L2+=str(rn.randint(0,1000))
    for i in usn:
        j=ord(i)
        if len(L2)<200:
            rn.seed(j)
            L2+=str(rn.randint(0,10000))
             
    #encrypting contents using key 3 and storing it in usn.dat
    encrypt(key3,usn,contents)
    #now we must encrypt key3 using key2 and store it in L2
    encrypt(key2,L2,key3)
    #then we must encrypt key2 using key1 and store it in L1
    encrypt(key1,L1,key2)
    print("Saved")

    
def login():
    import random as rn
    #here, we only know the usn and password cause we cant ask them to enter everything again...
    #its basically decrypt but instead of printing the contents at the end, we append to the file.
    #why cant we just append? we need key 3 to encrypt it and we need key 2 to open and read key 3.
    #hence, we need to decrypt everything except the contents in order to append to the users file in a readable way...
    contents,key1,key2,key3,usn,pwd,L1,L2='','','','','','','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\'
    while usn=='':
        usn=input("Enter your username: ")
    while pwd=='':
        pwd=input("Enter your password: ")
    while contents=='':
        contents=input("Enter the contents to be entered: ")
    for i in pwd:#remaking key 1
        for j in range(ord(i)*2):
            rn.seed(j)
            t=str(rn.randint(0,1000))
            key1+=t
    rn.seed(ord(key1[0])+int(key1[-1]))
    t=rn.randint(0,len(key1)//2)
    key1=key1[t::]
    if len(key1)>2000:
        key1=key1[0:2000]
   #remaking L1 (name), stores key 2
    for i in usn:
        j=ord(i)
        if len(L1)<100:
            rn.seed(j)
            L1+=str(rn.randint(0,10000))
    for i in key1:
        if len(L1)<200:
             rn.seed(i)
             L1+=str(rn.randint(0,10000))
    #decrypting key 2 from L1 using key 1
    key2=decrypt(key1,L1)
    #remaking L2 (name), contains key 3
    L2+=key2[-1]
    for i in key2:
        if len(L2)<100:
             rn.seed(i)
             L2+=str(rn.randint(0,1000))
    for i in usn:
        j=ord(i)
        if len(L2)<200:
            rn.seed(j)
            L2+=str(rn.randint(0,10000))
             
    #decrypting key 3 from L2 using key 2
    key3=decrypt(key2,L2)
    #encrypting contents using key 3 and storing it in usn.dat
    con=decrypt(key3,usn)
    con+=contents
    encrypt(key3,usn,con)
    print("Saved")


def read():
    import random as rn
    contents,key1,key2,key3,usn,pwd,L1,L2='','','','','','','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\'
    while usn=='':
        usn=input("Enter your username: ")
    while pwd=='':
        pwd=input("Enter your password: ")
    for i in pwd:#remaking key 1
        for j in range(ord(i)*2):
            rn.seed(j)
            t=str(rn.randint(0,1000))
            key1+=t
    rn.seed(ord(key1[0])+int(key1[-1]))
    t=rn.randint(0,len(key1)//2)
    key1=key1[t::]
    if len(key1)>2000:
        key1=key1[0:2000]
    #remaking L1 (name), stores key 2
    for i in usn:
        j=ord(i)
        if len(L1)<100:
            rn.seed(j)
            L1+=str(rn.randint(0,10000))
    for i in key1:
        if len(L1)<200:
             rn.seed(i)
             L1+=str(rn.randint(0,10000))
    #decrypting key 2 from L1 using key 1
    key2=decrypt(key1,L1)
    #remaking L2 (name), contains key 3
    L2+=key2[-1]
    for i in key2:
        if len(L2)<100:
             rn.seed(i)
             L2+=str(rn.randint(0,1000))
    for i in usn:
        j=ord(i)
        if len(L2)<200:
            rn.seed(j)
            L2+=str(rn.randint(0,10000))
    #decrypting key 3 from L2 using key 2
    key3=decrypt(key2,L2)
    #decrypting contents from usn.dat using key 3
    contents=decrypt(key3,usn)
    print(contents)

def delete():
    a=input("Are you sure you want to delete your file? (Y/N): ")
    if a.upper() in "YES":
        import random as rn
        contents,key1,key2,key3,usn,pwd,L1,L2='','','','','','','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\','C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt\\storage python code\\'
        while usn=='':
            usn=input("Enter your username: ")
        while pwd=='':
            pwd=input("Enter your password: ")
        for i in pwd:#remaking key 1
            for j in range(ord(i)*2):
                rn.seed(j)
                t=str(rn.randint(0,1000))
                key1+=t
        rn.seed(ord(key1[0])+int(key1[-1]))
        t=rn.randint(0,len(key1)//2)
        key1=key1[t::]
        if len(key1)>2000:
            key1=key1[0:2000]
        #remaking L1 (name), stores key 2
        for i in usn:
            j=ord(i)
            if len(L1)<100:
                rn.seed(j)
                L1+=str(rn.randint(0,10000))
        for i in key1:
            if len(L1)<200:
                 rn.seed(i)
                 L1+=str(rn.randint(0,10000))
        #decrypting key 2 from L1 using key 1
        key2=decrypt(key1,L1)
        #remaking L2 (name), contains key 3
        L2+=key2[-1]
        for i in key2:
            if len(L2)<100:
                 rn.seed(i)
                 L2+=str(rn.randint(0,1000))
        for i in usn:
            j=ord(i)
            if len(L2)<200:
                rn.seed(j)
                L2+=str(rn.randint(0,10000))

        import os
        os.remove(f'{usn}.dat')
        os.remove(f'{L1}.dat')
        os.remove(f'{L2}.dat')
        print("Files deleted.")
    else:
        pass
        
sign=''
while sign=='':#cant have an empty
    sign=input("Signup/Login/Read/Delete: ")
if sign.upper()=='SIGNUP':
    signup()
elif sign.upper()=='LOGIN':
    login()
elif sign.upper()=='DELETE':
    delete()
else:
    read()

'If there was a csv file with all usernames, passwords and answers, we can traverse it in a loop using signup and make files for all of them.'
