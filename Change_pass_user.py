# Change password or username

import Encryption 
# encrypt, decrypt, make_code, WeakCodeError : encrypt(data, int(code))

import os


def all_encrypted_files():
    things = os.listdir()
    files = []
    for file in things:
        if ".SDE" in file:
            files.append(file)
    return files


def change_password(new_password, old_password):
    # When this function is called all the files should be
    # in the CWD.

    '''
    call this function like:
        for file_completed_number, file_name in change_password():
            pass
    '''
    new_password, old_password = int(new_password), int(old_password)
    files = all_encrypted_files()

    copied_but_error = []

    for num, file in enumerate(files, start=1):

        try:
            with open(file) as old_file:
                old_data = old_file.read()

            copy_file = "ocod-"+file
            with open(copy_file, 'w') as copy_file:
                copy_file.write(old_data)

        except Exception as e:
            print(e)
            yield (-1, file)
            # -1 means a copy could not be generated

        else: 
            try:
                with open(file, 'w') as new_file:
                    new_file.write(Encryption.encrypt(Encryption.decrypt(old_data, old_password), new_password))
            except Exception as e:
                print(e)
                copied_but_error.append(copy_file)
                yield (-2, file)

                # -2 means a copy WAS generated but a new file was not.

            else:
                yield (num, file)


    for file in files:
        file = "ocod-"+file
        if file not in copied_but_error:
            os.remove(file)



def change_username(new_username, old_username):

    # username be like : Suchith-SDE (FOLDER NAME TOO)
    # both old and new user name has to be provided with -SDE

    # if "-SDE" not in old_username or "-SDE" not in new_username:
    #   print('The folder name was not provided according to rules')
    #   raise ValueError  

    my_path = os.getcwd()
    os.chdir("../")
    try:
        os.rename(old_username, new_username)
    except Exception as e:
        print(e)
        os.chdir(my_path)
        return False
    else:
        os.chdir(new_username)
        return True













