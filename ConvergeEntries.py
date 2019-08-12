import os
from Open_drive import open_file


def SDE_files():
    original_path = os.getcwd()
    files = os.listdir()
    files2 = []
    for file in files:
        if file[-4:] == ".SDE":
            files2.append(os.path.abspath(file))

    return files2


def blank(text):
    return text


def write_new_file(files, function=blank,
                   folder=None, *args, **kwargs):
    ''' The function passed as an argument should always take the first
    parameter as text and the function should always return text
    the additional parameters can be passed as args and kwargs
    function is called like : function(text, *args, **kwargs)'''
    original_path = os.getcwd()
    try:
        if folder is not None:
            os.chdir(folder)
        else:
            folder = os.getcwd()

        try:
            our_folder = "Compiled Files"
            os.makedirs(our_folder)
        except FileExistsError:
            pass
        finally:
            os.chdir(our_folder)

        limit = 1000
        part = 1
        count = 0
        file_no = 0
        flag = False

        while not flag:
            with open(str(part).zfill(2)+"Compiled Files.txt", 'w') as f:
                while True:

                    if file_no >= len(files):
                        flag = True
                        break

                    if "datfile" not in files[file_no] and 'spellcheck' not in files[file_no]:
                        count += f.write("\n")
                        count += f.write("-"*50)
                        name = os.path.basename(files[file_no])
                        count += f.write("\n"+(name)[:name.index(".")]+"\n")
                        count += f.write("-"*50)
                        count += f.write("\n")

                        with open(files[file_no]) as rf:
                            count += f.write(function(rf.read().strip(),
                                                      *args, **kwargs))

                    file_no += 1

                    if count >= limit:
                        if file_no >= len(files):
                            flag = True
                            break

                        part += 1
                        count = 0
                        break
        open_file(folder)
    finally:
        os.chdir(original_path)


# write_new_file(SDE_files(), new_file="Compiled File.txt", code=2808)
