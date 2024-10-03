#Works for up to 10,000 characters to be encrypted.

class Small_trivial_functions():
    def warn_first_time_user():
        print("If this is your first time running this code, got to this directory *C:\\Users\\HP\\OneDrive\\Desktop\\Comp stuff\\encrypt* and create a file called *storage python code* if it does not exist")
    
    def signup_input_valid_username():
        usn=input("Enter your username: ")

        try:
            check=open(f'{usn}.dat','rb')
            check.close()

            print('Username aldready taken. Login instead? (y/n): ')
            if input('')=='y':
                input_choice()
            else:
                return(Small_trivial_functions.signup_input_valid_username())
    
        except FileNotFoundError:
            return(usn)

    def login_input_valid_username():
        usn=input("Enter your username: ")
        try:
            check=open(f'{usn}.dat','rb')
            check.close()
            return(usn)
        except FileNotFoundError:
            print('Username not found. Signup instead? (y/n): ')
            if input('')=='y':
                input_choice()
            else:
                return(Small_trivial_functions.login_input_valid_username())
    
    def input_valid_password():
        pwd=input("Enter your password: ").strip()

        if len(pwd)<8:
            print("Password must be more than 8 characters with no spaces.")
            return(Small_trivial_functions.input_valid_password())
        else:
            return(pwd)

    def input_contents():
        return(input("Enter the contents of the file: "))

    def input_valid_answer(question):
        answer=input(question)
        if len(answer)<8:
            print("Answer needs to be atleast 8 characters long.")
            return(Small_trivial_functions.input_valid_answer(question))
        else:
            return(answer)

    def delete_file(file):
        import os
        os.remove(f'{file}.dat')


class generators():

    def generate_key(source_obj):
        #the numbers in this function are experimental and do not hold special significance.
        import random

        key=''
        for i in source_obj:
            for j in range(ord(i)*2):

                random.seed(j)
                t=str(random.randint(0,1000))
                key+=t

        random.seed(ord(key[0])+int(key[-1]))
        t=random.randint(0,len(key)//2)
        key=key[t::]

        if len(key)>2000:
            key=key[0:2000]

        return(key)
        
    def address_generator(key,usn): 
        #the numbers in this function are experimental and do not hold special significance.
        import random 
        location='storage python code\\' #directory to build upon 

        for i in usn:
            j=ord(i)
            if len(location)<100:
                random.seed(j)
                location+=str(random.randint(0,10000))

        for i in key:
            if len(location)<200:
                random.seed(i)
                location+=str(random.randint(0,10000))

        return(location)


class encryption(): #TODO could divide into sublclasses, encrypt and decrypt for the trivial functions?
    class encrypt():
        def fill_list_with_ascii_of_contents(contents):
            out_list=[]
            
            for i in contents:
                out_list.append(ord(i))
            return(out_list)
            
        def pickle_list_here(list_to_encrypt,location):
            import pickle

            file=open(f'{location}.dat','wb')
            pickle.dump(list_to_encrypt,file)
            file.close()
            
        def get_raw_pickled_data_from(location):
            file=open(f'{location}.dat','r',encoding='iso-8859-15')
            contents=file.read()
            file.close()

            return contents

    def get_number_to_add(key,count,odd_or_even,check):
            try:
                number_to_add = int(key[count]) 
            except IndexError:
                count = 0
                number_to_add = int(key[count])
            count+=1

            if odd_or_even%2==check:
                number_to_add=0-number_to_add

            return(number_to_add,count)

    def substitute(key,outgoing_list,check):
        count=0
        #most numbers here are experimental and hold no special significance.
        for i in range(int(key[1])):
            for j in range(len(outgoing_list)):
                number_to_add,count=encryption.get_number_to_add(key,count,i,check) #check=1 for encrypt, check=0 for decrypt
                outgoing_list[j]=outgoing_list[j]+number_to_add
        return(outgoing_list)

    def key_encrypts_stores(key,contents,Location):

        #TODO come up with better names for each final_changing_list?
        final_changing_list = encryption.encrypt.fill_list_with_ascii_of_contents(contents)
        
        final_changing_list = encryption.substitute(key,final_changing_list,1)

        encryption.encrypt.pickle_list_here(final_changing_list,'store')
        contents=encryption.encrypt.get_raw_pickled_data_from('store')

        final_changing_list=encryption.encrypt.fill_list_with_ascii_of_contents(contents)

        final_changing_list=encryption.substitute(key[::-1],final_changing_list,1)#reversing key has no specifial significance. 

        Small_trivial_functions.delete_file('store')

        encryption.encrypt.pickle_list_here(final_changing_list,Location)
        
    class decrypt():
        def get_unpickled_data_from(Location):
            import pickle
            try:
                file=open(f'{Location}.dat','rb')
                outgoing_list=pickle.load(file)
                file.close()
            except FileNotFoundError:
                print("Wrong username or password.")
                exit()
            
            return(outgoing_list)
        
        def get_characters_of_ascii_list(given_list):
            data=''
            for i in given_list:
                data+=str(chr(i))
            
            return(data)
        
        def write_data_in(data,Location):
            file=open(f'{Location}.dat','w',encoding='iso-8859-15')
            file.write(data)
            file.close()

    def key_decrypts_from(key,Location): #TODO come up with better name than final_changing_list and data.
        import pickle

        final_changing_list=encryption.decrypt.get_unpickled_data_from(Location)

        final_changing_list = encryption.substitute(key[::-1],final_changing_list,0)
    
        content = encryption.decrypt.get_characters_of_ascii_list(final_changing_list)

        encryption.decrypt.write_data_in(content,'store')
        final_changing_list = encryption.decrypt.get_unpickled_data_from('store')

        final_changing_list = encryption.substitute(key,final_changing_list,0)
        
        content = encryption.decrypt.get_characters_of_ascii_list(final_changing_list)

        Small_trivial_functions.delete_file('store')

        return(content)


def make_all_keys(pwd):
    first_key = generators.generate_key(pwd)
    second_key = generators.generate_key(Small_trivial_functions.input_valid_answer("Enter the name of your first school: "))
    third_key = generators.generate_key(Small_trivial_functions.input_valid_answer("Enter your first nickname: "))
    return(first_key,second_key,third_key)

def signup():

    Small_trivial_functions.warn_first_time_user()

    usn = Small_trivial_functions.signup_input_valid_username()
    pwd = Small_trivial_functions.input_valid_password()
    contents = Small_trivial_functions.input_contents()
    
    first_key, second_key, third_key = make_all_keys(pwd)
    
    location_second_key = generators.address_generator(first_key,usn)
    location_third_key = generators.address_generator(second_key,usn)


    encryption.key_encrypts_stores(third_key, contents, usn)
    encryption.key_encrypts_stores(second_key, third_key, location_third_key)
    encryption.key_encrypts_stores(first_key, second_key, location_second_key)

    print("Saved")
    
def add():
    usn = Small_trivial_functions.login_input_valid_username()
    pwd = Small_trivial_functions.input_valid_password()
    contents_to_add = Small_trivial_functions.input_contents()
    
    first_key = generators.generate_key(pwd)

    location_second_key = generators.address_generator(first_key,usn)
    second_key = encryption.key_decrypts_from(first_key, location_second_key)

    location_third_key = generators.address_generator(second_key,usn)
    third_key = encryption.key_decrypts_from(second_key, location_third_key)
    
    existing_contents = encryption.key_decrypts_from(third_key, usn)

    final_contents = existing_contents+' '+contents_to_add
    encryption.key_encrypts_stores(third_key, final_contents, usn)

    print("Saved")

def read():
    usn = Small_trivial_functions.login_input_valid_username()
    pwd = Small_trivial_functions.input_valid_password()

    first_key = generators.generate_key(pwd)

    location_second_key = generators.address_generator(first_key,usn)
    second_key = encryption.key_decrypts_from(first_key, location_second_key)

    location_third_key = generators.address_generator(second_key,usn)
    third_key = encryption.key_decrypts_from(second_key, location_third_key)
    
    existing_contents = encryption.key_decrypts_from(third_key, usn)
    
    print(existing_contents)

def delete():
    a=input("Are you sure you want to delete your file? (Y/N): ")
    if a.upper() in "YES":
        
        usn = Small_trivial_functions.login_input_valid_username()
        pwd = Small_trivial_functions.input_valid_password()

        first_key = generators.generate_key(pwd)

        location_second_key = generators.address_generator(first_key,usn)
        second_key = encryption.key_decrypts_from(first_key, location_second_key)

        location_third_key = generators.address_generator(second_key,usn)

        Small_trivial_functions.delete_file(usn)
        Small_trivial_functions.delete_file(location_second_key)
        Small_trivial_functions.delete_file(location_third_key)

        print("File deleted succesfully.")
        
    else:
        input_choice()


def input_choice():
    choice=input("Signup/Add/Read/Delete: \n").upper()
    if choice == 'SIGNUP':
        signup()
    elif choice == 'ADD':
        add()
    elif choice == 'DELETE':
        delete()
    elif choice == 'READ':
        read()
    else:
        print("Please choose one of the below: ")
        input_choice()

input_choice()
