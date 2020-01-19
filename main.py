from Encryption import encrypt, decrypt, make_code, WeakCodeError
import datetime
from tkcalendar import Calendar
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import os
import time
import random
from Open_drive import save_to_drive, open_file
from ConvergeEntries import write_new_file, SDE_files
import pickle
import traceback
import Change_pass_user

'''
Things to be addded :

- The editing the spell_dict after user enters new dict.

'''

# ------------------- Loading of the application -------------------------


'''
    Color Pallet:
    # 58afd0
    # 489fd0
    # 388fd0
    # 287fd0
    # 186fd0
'''
w = 800
h = 600
main_folder = "Diary_Entries-SDE"
current_date = ''
base_color = '#4d94ff'
text_base = base_color  # D1EEEE'
original_path = os.getcwd()
original_path_1 = original_path
Application_Name = "Journal SDE 1.5.0"
# Later used while saving the diary entries


# Fonts ---------
FONT = ("Verdana", 12)
FONT_BOLD = ("Verdana bold", 12)
# FONT1 = ("Arial", 12)
# FONT2 = ("Comic Sans MS", 22)

date_font = ("Verdana", 17)
calender_font = FONT
text_box_font = FONT
opt_font = ("Verdana bold", 30)
opts_label_font = ("Verdana bold", 14)
# ------------------------------

code = 0
user = ''

# -------------------- test values

# code = 1212
# user = 'Testing-SDE'


# ----- Spell check dict ----

spell_check_file = 'spellcheck.SDE'

spells_dict = {
    'i': 'I',
    "dont": "don't",
    "im": "I'm",
    "cant": "can't",
    'ill': "I'll",
    'ive': "I've"
}

widgets = {}


def load_spells_file():
    global spells_dict
    try:
        file = open(spell_check_file, 'rb')
        spells_dict = pickle.load(file)
        file.close()
    except:
        pass


def save_spells_file():
    if os.path.isfile(spell_check_file):
        with open(spell_check_file, 'wb') as pickel_out:
            pickle.dump(spells_dict, pickel_out)

# ---------------------------


upper_bg = '#0066ff'  # "#a31aff"
cal_bg = '#002966'  # '#2e004d'
cal_text = '#005ce6'  # '#c266ff'
ex_text = '''potbnijeg8ufhvbivjsbdgof'''

cal_variable = None

instruction_to_save_to_drive = '''
1) The files in their encrypted version will be zipped
2) The folder in which the zip exists WILL BE OPENED
3) Google Drive Website will be opened
4) You have to upload the file MANUALLY to drive
'''


def preset_window(app_window):
    app_window.configure(bg=base_color)
    # Import to change geometry before centering
    center(app_window)

    with FolderManager(original_path_1):
        app_window.iconbitmap(resource_path('Diary_icon.ico'))

    app_window.title(Application_Name)
    app_window.focus()
    pass


class FolderManager:
    # A simple context manager to change in and out of
    # a folder
    def __init__(self, folder):
        self.folder = folder

    def __enter__(self):
        self.main = os.getcwd()
        os.chdir(self.folder)

    def __exit__(self, exc_type, exc_val, traceback):
        os.chdir(self.main)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    To be able to get the images to work in One File mode"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_cal_date(cal):
    # Returns the date selected on the calender widget
    var = cal.selection_get()
    if var is None:
        raise Exception
    else:
        return var


def center(win):
    # Center a window in the screen
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def check_folder(folder):
    # Checks if the folder exists
    return os.path.isdir(folder)


def check_file(date):
    # Checks if the file exists
    try:
        open(date + ".SDE")
        return True
    except FileNotFoundError:
        return False


def caldates():
    # x = datetime.datetime(2020, 5, 17)
    files = files_in_folder()

    dates = []
    for file in files:
        try:
            day = datetime.datetime(int(file[0]),
                                    int(file[1]),
                                    int(file[2]))
            dates.append(day)
        except:
            continue

    return dates


def save_data(file_date, text_box):
    data = text_box.get('0.0', 'end')
    # Get the text that has been entered into the box

    data = data.rstrip()

    data = spell_check(data)

    if data.strip() == "":
        # Don't save an empty file
        return None

    if data.strip().lower() == "delete":
        try:
            os.remove(file_date + ".SDE")
            return None
        except FileNotFoundError:
            return None

    data = encrypt(data, int(code))
    # Encrypt the data before saving as a file

    with open(file_date + ".SDE", 'w') as file:
        file.write(data)


def add_markings(calender):
    dates = caldates()
    calender.calevent_remove("all")
    for date in dates:
        calender.calevent_create(date, 'completed', 'done')

    calender.tag_config('done', background='#58afd0', foreground='black')


def set_notepad(cal, day_var, text_box):
    # This functions retrieves the diary entry of the selected
    # date on the calender and puts it into the text box
    global current_date
    cal_date = get_cal_date(cal)
    date = cal_date.strftime("%Y-%m-%d")
    # .strftime is a method of the datetime.datetime class and it returns
    # a string of the date obj according to the required format
    day = cal_date.strftime("%d %B %Y, %A")
    day_var.set(day)

    # When user wants to change to a different date
    # SAVE CURRENT ENTRY ----> CLEAR THE TEXT BOX ---> INSERT ENTRY OF NEW DATE
    save_data(current_date, text_box)
    text_box.delete(1.0, 'end')
    current_date = date
    add_markings(cal)

    if check_file(date):

        date += ".SDE"

        with open(date) as file:
            data = file.read()

        data = decrypt(data, int(code)).rstrip()
        # decrypts the encrypted data stored in the files
        text_box.insert('end', data)
        # Inserts the entry of that day
    text_box.focus()


def cal_set(root):
    global cal_variable, widgets
    # Calender widget
    today = (today_date_num('m') + "/"
             + today_date_num('d') + "/" + today_date_num('y'))
    cal_variable.set(today)
    cal = Calendar(root, font=calender_font, selectmode='day',
                   textvariable=cal_variable,
                   firstweekday="sunday",
                   showweeknumbers=False,
                   background=cal_bg,
                   headersbackground=cal_text,
                   weekendforeground='black',
                   showothermonthdays=False,
                   othermonthforeground='#bfbfbf',
                   othermonthbackground='#d9d9d9',
                   othermonthweforeground='#bfbfbf',
                   othermonthwebackground='#d9d9d9')
    cal.place(x=10, y=150, w=380, h=300)

    widgets["CAL"] = cal
    return cal


def today_date_num(option):
    # Get today's date in single number form
    today = datetime.date.today()
    if option == "m":
        return today.strftime("%m")
    elif option == 'd':
        return today.strftime("%d")
    elif option == 'y':
        return today.strftime("%Y")
    else:
        raise TypeError


def today_date():
    # Today's date in proper format
    today = datetime.date.today()
    d1 = today.strftime("%d %B %Y            %A")
    return d1


def read_to_textbox(text_box, file):
    if ".SDE" not in file:
        file += ".SDE"
    text_box.delete(1.0, 'end')
    try:
        with open(file) as f:
            data = decrypt(f.read(), int(code))
        text_box.insert('end', data)
    except FileNotFoundError:
        return False
    else:
        return True


def save_to_file(text_box, file):
    if ".SDE" not in file:
        file += ".SDE"
    data = text_box.get('0.0', 'end')
    with open(file, 'w') as f:
        f.write(encrypt(data, int(code)))


def notes_func(text_box):
    global current_date
    file = "notes"
    if current_date == file:
        # When notes is already open
        return None
    save_data(current_date, text_box)
    current_date = file

    if not read_to_textbox(text_box, file):
        # The file did not exist
        with open(file + ".SDE", 'w') as f:
            f.write(encrypt("--- ADD NOTES HERE ---\n\n", int(code)))

        read_to_textbox(text_box, file)


def spell_check(text):
    exceptions = '<>?/\\{}()"\'!@#$%^&*_+=|`~:;.,'
    lines = text.split("\n")
    first_word_caps = True
    next_word_caps = False
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")
        # now lines is a list all lines where each line is a list of words
        line = lines[i]
        if line == [""]:
            # Make the next line letter caps
            first_word_caps = True
            continue

        for index, word in enumerate(line):
            if word == "":
                continue

            if word.isupper():
                upper = True

            else:
                upper = False

            original_word = word
            for j in exceptions:
                word = word.strip(j)
            word_start = original_word.index(word)
            if first_word_caps:
                make_title = True
                first_word_caps = False
                next_word_caps = False
            elif next_word_caps:
                make_title = True
                next_word_caps = False
            elif word.istitle():
                make_title = True
            else:
                make_title = False
            word = word.lower()

            try:
                if word[0] == "i" and word[1] == "'":
                    i_cat = True
                else:
                    i_cat = False
            except IndexError:
                i_cat = False

            if word in spells_dict:
                before_part = original_word[:word_start]
                after_part = original_word[word_start + len(word):]
                for item in ".;!?":
                    if item in before_part:
                        make_title = True

                replacement = spells_dict[word]
                if make_title:
                    replacement = replacement.capitalize()
                line[index] = before_part + replacement + after_part
            else:
                if make_title:
                    line[index] = line[index].capitalize()
                elif upper:
                    line[index] = line[index].upper()
                elif i_cat:
                    line[index] = line[index].capitalize()
                else:
                    line[index] = line[index].lower()

            if line[index][-1] in ".;":
                next_word_caps = True

    for i in range(len(lines)):
        lines[i] = " ".join(lines[i])
    new_text = "\n".join(lines)

    return new_text


def make_today():
    global cal_variable, current_date
    today = (today_date_num('m') + "/"
             + today_date_num('d') + "/" + today_date_num('y'))
    cal_variable.set(today)
    cal_variable.set(today)


def change_page(app, cal, day_var, text_box):
    set_notepad(cal, day_var, text_box)
    app.show_frame(OptionsPage)


def set_left_frame(root, app, text_box):
    global current_date, cal_variable, widgets
    day_var = tk.StringVar()
    # Only the variable change whenever needed
    current_date = (today_date_num('y')) + "-" + \
        (today_date_num('m')) + "-" + (today_date_num("d"))

    day_var.set(today_date())

    cal_variable = tk.StringVar()
    cal = cal_set(root)

    def change_day(*args, **kwargs):
        set_notepad(cal, day_var, text_box)

    cal_variable.trace('w', change_day)

    refresh_but = ttk.Button(root, text="Refresh")
    refresh_but.config(command=lambda: set_notepad(cal, day_var, text_box))
    # Import button if the day needs to be changed
    refresh_but.place(x=25, y=470, w=170, h=50)
    widgets["REF"] = refresh_but

    notes_but = ttk.Button(root, text="Notes")
    notes_but.config(command=lambda: notes_func(text_box))
    notes_but.place(x=205, y=470, w=170, h=50)
    widgets["NOTE"] = notes_but

    options_button = ttk.Button(root, text="Options")
    options_button.config(command=lambda: change_page(
        app, cal, day_var, text_box))
    options_button.place(x=110, y=530, w=150 + 30, h=50)
    widgets["OPTS"] = options_button

    next_button = ttk.Button(root, text="Next")
    next_button.config(command=lambda: next_page(cal, day_var, text_box))
    next_button.place(x=300, y=530, w=50, h=50)
    widgets["NEXT"] = next_button

    prev_button = ttk.Button(root, text="Prev")
    prev_button.config(command=lambda: prev_page(cal, day_var, text_box))
    prev_button.place(x=50, y=530, w=50, h=50)
    widgets["PREV"] = prev_button

    today_button = ttk.Button(root, text="Today")
    today_button.config(command=make_today)
    today_button.place(x=275, y=115, w=100, h=25)
    widgets["TDAY"] = today_button

    # This is the Dark purple bar that is created of design purposes
    frame = tk.Frame(root, bg=upper_bg)
    frame.place(x=0, y=0, w=w // 2, h=100)
    widgets["UBG"] = frame

    label = tk.Label(frame, textvariable=day_var, wraplength=250)
    # comics----------------------------------------------------------
    label.config(bg=upper_bg, font=date_font, fg='white')
    label.place(x=10, y=40)
    widgets["DATE"] = label

    set_notepad(cal, day_var, text_box)


def files_in_folder():
    things = os.listdir()
    files = []
    for file in things:
        if "-" in file and ".SDE" in file:
            file = file.replace(".SDE", "")
            files.append(file)

    files.sort()

    for i in range(len(files)):
        files[i] = files[i].split("-")
        # file.reverse() # This reverse Causes dd-mm-yyyy
    return files


def next_page(cal, day_var, text_box):
    global cal_variable, current_date
    files = files_in_folder()
    for i in range(len(files)):
        files[i] = "/".join(files[i])

    cur = ("/".join(current_date.split("-")))

    for file in range(len(files)):
        if files[file] > cur:
            set_date = files[file].split("/")

            set_date = set_date[1] + "/" + set_date[2] + "/" + set_date[0]

            cal_variable.set(set_date)
            cal_variable.set(set_date)
            return None
    else:
        return None


def prev_page(cal, day_var, text_box):
    global cal_variable, current_date
    files = files_in_folder()
    for i in range(len(files)):
        files[i] = "/".join(files[i])

    cur = ("/".join(current_date.split("-")))

    for file in range(len(files) - 1, -1, -1):
        if files[file] < cur:
            set_date = files[file].split("/")

            set_date = set_date[1] + "/" + set_date[2] + "/" + set_date[0]

            cal_variable.set(set_date)
            cal_variable.set(set_date)
            return None
    else:
        return None


def set_right_frame(root):
    s = tk.Scrollbar(root, orient=tk.VERTICAL)
    # Setting a scroll bar in case needed
    text = tk.Text(root, wrap=tk.WORD, yscrollcommand=s.set)
    # The height and width is based on the font-size and not pixels
    # It has word wrap functionality added onto it.
    text.config(font=text_box_font)
    text.place(x=w // 2, y=2, w=w // 2 - 18, h=h - 4)
    text.focus()
    widgets["TEXT"] = text
    s.config(command=text.yview)
    # Setting what the scroll bar scrolls
    # The scroll bar is pointless if not set
    s.place(x=w - 17, y=0, height=h)
    widgets["SCROLL"] = s

    # return text; to return the textbox to edit later
    return text


def last_func(root, file_date, text):
    # The function performed just before closing the window
    try:
        save_data(file_date, text)
        save_spells_file()
    except Exception as e:
        pop_up = tk.Toplevel(root)
        pop_up.geometry('600x600')
        preset_window(pop_up)
        error_msg = "Error before closing\nwindow\nplease report:\n" + str(e)
        tk.Label(pop_up, text=error_msg).pack()
        pop_up.update()

        file = "ErrorMSG--Journal.txt"

        with open(file, 'w') as f:
            f.write(error_msg + "\n")
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            f.write(traceback_str)

        open_file(file)

        time.sleep(2)
    finally:
        root.destroy()


class MainApp(tk.Tk):

    def __init__(self, pages, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self)

        main_frame.pack(side="top", fill="both", expand=True)

        main_frame.grid_rowconfigure(0, weight=1)
        # 0 --> minimum size
        # weight =1 --> priority thing
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.bind('<Configure>', on_resize)

        self.frames = {}

        # pages is a list of pages
        for F in pages:
            frame = F(main_frame, self)
            # Here self is just the parent/ root
            self.frames[F] = frame
            frame.configure(bg=base_color)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(pages[0])

    def show_frame(self, page):
        global CURRENT_PAGE
        self.frames[page].tkraise()
        width = self.winfo_width()
        height = self.winfo_height()
        CURRENT_PAGE = page.page_name
        on_resize(FakeEvent(w=width, h=height))


class MainPage(tk.Frame):

    page_name = "MainPage"

    def __init__(self, main_frame, root):
        tk.Frame.__init__(self, main_frame)

        text = set_right_frame(self)
        set_left_frame(root=self, app=root, text_box=text)
        root.protocol('WM_DELETE_WINDOW', lambda: last_func(
            root, current_date, text))


class OptionsPage(tk.Frame):

    page_name = "OptionsPage"

    def __init__(self, main_frame, root):
        tk.Frame.__init__(self, main_frame)
        button = ttk.Button(self, text="Back",
                            command=lambda: root.show_frame(MainPage))
        button.place(x=400 - 100, y=600 - 75, h=50, w=200)

        widgets["OPTS_BACK"] = button

        set_options_page(self)


def make_options(frame):
    global spells_dict, code, widgets

    def save_drive():
        def button_func():
            window.destroy()
            save_to_drive()

        window = tk.Toplevel(frame)

        for line in instruction_to_save_to_drive.split("\n"):
            instr = tk.Label(window, text=line)
            instr.config(font=FONT_BOLD, bg=base_color, fg='white', anchor="w")
            instr.pack(fill=tk.X)
        ttk.Button(window, text='  OK  ', command=button_func).pack(pady=5)

        preset_window(window)

    def export():
        folder = filedialog.askdirectory()
        if folder != '':

            if os.path.exists(folder):
                try:
                    write_new_file(SDE_files(), function=decrypt,
                                   folder=folder, code=code)
                except Exception as e:
                    traceback.print_exc()
                    window(frame, "Close", str(e))
                window(frame, "DONE")

    def spell_check_opts():
        global spells_dict

        def insert_spells():
            string = ''
            key_value = list(spells_dict.items())
            key_value.sort()
            for word, correction in key_value:
                string += word + " ---> " + correction + "\n"

            spells_box.insert("end", string)

        def update_spells():
            global spells_dict
            data = spells_box.get('0.0', 'end')
            data = data.strip()

            # ["cant ---> can't\ndont ---> <don't>\n<i> ---> <I>\n
            # <ill> ---> <I'll>\n<im> ---> <I'm>\n<ive> ---> <I've>"]

            try:
                data = data.split("\n")
                spells_new_dict = {}

                for spell_corrects in data:
                    if spell_corrects.count("--->") != 1:
                        raise Exception

                    spell_corrects = spell_corrects.split("--->")
                    spells_new_dict[spell_corrects[0].strip()
                                    ] = spell_corrects[1].strip()

                spells_dict = spells_new_dict

            except Exception as e:
                window(frame, "Close", 'Wrong Format')

            spells_window.destroy()

        # Create the file here if not existing
        # Dont need to make a file if not necessary
        if not os.path.isfile(spell_check_file):
            with open(spell_check_file, 'wb') as f:
                pickle.dump(spells_dict, f)

        spells_window = tk.Toplevel(frame)
        spells_window.geometry('350x450')
        spells_window.resizable(False, False)

        s = tk.Scrollbar(spells_window, orient=tk.VERTICAL)
        # Setting a scroll bar in case needed
        spells_box = tk.Text(spells_window, wrap=tk.WORD, yscrollcommand=s.set)
        # The height and width is based on the font-size and not pixels
        # It has word wrap functionality added onto it.
        spells_box.config(font=text_box_font)
        spells_box.place(x=5, y=5, w=350 - 30, h=400 - 10)
        spells_box.focus()
        s.config(command=spells_box.yview)
        # Setting what the scroll bar scrolls
        # The scroll bar is pointless if not set
        s.place(x=5 + 350 - 30, y=5, height=400 - 10)

        button = ttk.Button(spells_window, text='SAVE', command=update_spells)
        button.place(x=5, y=405, w=340, h=40)

        preset_window(spells_window)
        insert_spells()
        spells_window.mainloop()

    def all_entries():
        def button_func():
            window.destroy()

        window = tk.Toplevel(frame)
        window.geometry('250x400')

        listbox = tk.Listbox(window)
        listbox.config(font=FONT_BOLD, bg=base_color, fg='white')

        files = files_in_folder()
        for i in range(len(files)):
            files[i] = "#".join(files[i])

        files.sort()

        for i in range(len(files)):
            files[i] = " - ".join(reversed(files[i].split("#")))

        for i, file in enumerate(files):
            listbox.insert(i, file)

        listbox.place(x=10, y=10, w=230, h=350)

        ttk.Button(window, text='close', command=button_func).place(
            x=10, y=365, w=230)

        preset_window(window)

    def change_username():
        def button_func():
            global user
            new_username_str = str(new_username.get())
            if validate_values(win_pop, new_username_str, 1710):
                # The password does'nt matter its just
                # to validate the username
                cur_path = os.getcwd()
                os.chdir("../")
                if not check_user(new_username_str):
                    os.chdir(cur_path)
                    new_username_str = make_folder_name(new_username_str)
                    Change_pass_user.change_username(
                        new_username_str, user)
                    user = new_username_str
                    win_pop.destroy()
                    window(frame, "Done", label="")
                else:
                    os.chdir(cur_path)
                    window(win_pop, "Close", "User Already Exist")

        win_pop = tk.Toplevel(frame)
        win_pop.geometry('400x100')

        preset_window(win_pop)

        tk.Label(win_pop, text="New Username :", font=FONT_BOLD,
                 bg=base_color, fg='white').place(x=5, y=18)

        new_username = tk.StringVar()
        ent = tk.Entry(win_pop, textvariable=new_username)

        ent.place(x=160, y=20, w=225, h=25)

        ttk.Button(win_pop, text="Change",
                   command=button_func).place(x=90, y=60, w=225, h=30)

        win_pop.mainloop()

    def change_password():
        global code

        def r_u_sure():
            # Before confirming, check if old password is
            # correct and new one is valid
            old_code = old_password.get()
            new_code = new_password.get()
            cont = False
            if validate_values(window_pop, 'TestUser', old_code):
                # The Username does'nt matter its just
                # to validate the password
                if password_check(window_pop, old_code):
                    if validate_values(window_pop, 'TestUser', new_code):
                        cont = True

            if cont:
                pop_up = tk.Toplevel(window_pop)
                pop_up.geometry('200x100')
                confirm_but = ttk.Button(pop_up, text="Confirm",
                                         command=lambda:
                                         change_pass_ok(pop_up,
                                                        confirm_but,
                                                        new_code,
                                                        old_code))
                confirm_but.pack()
                preset_window(pop_up)
                pop_up.mainloop()

        def change_pass_ok(pop_up, confirm_but, new_code, old_code):
            global code
            confirm_but.destroy()
            label_var = tk.StringVar()
            label_var.set("Processing... Don't close")
            tk.Label(pop_up, textvariable=label_var).pack()
            mess_1 = []  # Could not copy
            mess_2 = []  # Copied but could not change

            for file_completed_number, file_name in (
                    Change_pass_user.change_password(new_code, old_code)):
                if file_completed_number == -1:
                    mess_1.append(file_name)
                if file_completed_number == -2:
                    mess_2.append(file_name)

            # Global Update
            code = int(new_code)
            window_pop.destroy()
            window(frame, "Done", label="Successfully Changed")

        window_pop = tk.Toplevel(frame)
        window_pop.geometry('400x150')

        preset_window(window_pop)

        tk.Label(window_pop, text="Old Password :", font=FONT_BOLD,
                 bg=base_color, fg='white').place(x=5, y=18)

        old_password = tk.StringVar()
        ent = tk.Entry(window_pop, textvariable=old_password, show="*")

        ent.place(x=160, y=20, w=225, h=25)

        tk.Label(window_pop, text="New Password :", font=FONT_BOLD,
                 bg=base_color, fg='white').place(x=5, y=48 + 10)

        new_password = tk.StringVar()
        ent = tk.Entry(window_pop, textvariable=new_password, show="*")

        ent.place(x=160, y=50 + 10, w=225, h=25)

        ttk.Button(window_pop, text="Change", command=r_u_sure).place(
            x=90, y=100, w=225, h=30)

        window_pop.mainloop()

    buttons = [
        'Save to Drive',
        'Export',
        'Spell Check',
        'Show All Entries',
        'Change UserName',
        'Change Password'
    ]
    texts = [
        'Save files to drive as zip',
        'Export entries as text file',
        'Add/Remove to words to spell check',
        'Show all DATES with entries',
        'Change UserName of current user',
        'Change Password of current user',
    ]
    commands = [
        save_drive,
        export,
        spell_check_opts,
        all_entries,
        change_username,
        change_password
    ]

    widgets["OPTS_BUTS"] = []
    widgets["OPTS_TEXTS"] = []

    for i, button in enumerate(buttons):
        t_button = ttk.Button(frame, text=button, command=commands[i])
        y = 100 + (i * 70)
        t_button.place(x=50, y=y, w=200, h=50)
        t_text = tk.Label(frame, text=texts[i])
        t_text.config(bg=upper_bg, font=opts_label_font, fg='white')
        t_text.place(x=275, y=y, w=500, h=50)
        widgets["OPTS_BUTS"].append(t_button)
        widgets["OPTS_TEXTS"].append(t_text)


def set_options_page(frame):
    global widgets

    label = tk.Label(frame, text="Options Page",
                     bg=upper_bg, font=opt_font,
                     fg='white')
    label.place(x=245, y=10)
    widgets["OPTS_LABEL"] = label

    buttons = make_options(frame)


class FakeEvent:
    def __init__(self, w, h):
        self.width = w
        self.height = h


def on_resize(event):
    w = event.width
    h = event.height

    if w < 300 or h < 300:
        # for some reason the width and height kept
        # becoming very low numbers even though the
        # actual window size remained big
        return None

    if CURRENT_PAGE == "MainPage":
        # Right-side
        wrap = w * 0.4

        x1r = 0.45
        x2r = 0.55

        y1r = 0.2
        y2r = 0.6
        y3r = 0.2

        th = 0.04  # today button ratio
        tw = 0.1

        widgets["TEXT"].place(x=w * x1r, y=0,
                              # 0.6 - 60%, -5 for scroll bar
                              w=int(w * x2r) - 15,
                              h=int(h))
        widgets["SCROLL"].place(x=w - 15, y=0, h=h)

        # Left-side
        widgets["UBG"].place(x=0, y=0,
                             w=int(w * x1r),
                             h=int(h * y1r))
        df = date_font
        widgets["DATE"].config(fg="white",
                               wraplength=wrap,
                               font=(df[0],
                                     int(df[1] * (w + h) / 2 * 0.0015) + 2))

        widgets["DATE"].place(x=0, y=0,
                              w=int(w * x1r),
                              h=int(h * y1r))

        widgets["TDAY"].place(x=(w * x1r) - (w * tw) - (10),
                              y=(h * 0.2) + (2),
                              w=int(w * tw),
                              h=int(h * th))
        buf = 10
        widgets["CAL"].place(x=buf / 2, y=(h * (y1r + th + 0.01)),
                             w=int(w * x1r) - buf,
                             h=int(h * (y2r - (th + 0.01))))

        math = ((w * x1r) / 2) - ((w * x1r) * 0.9 / 2) - (buf / 2)
        widgets["REF"].place(x=math, y=(h * (y2r + y1r)) + (buf / 2),
                             w=int((w * x1r) * 0.9 / 2),
                             h=int(h * (y3r / 2) - 10))
        math = ((w * x1r) / 2) + (buf / 2)
        widgets["NOTE"].place(x=math, y=(h * (y2r + y1r)) + (buf / 2),
                              w=int((w * x1r) * 0.9 / 2),
                              h=int(h * (y3r / 2) - 10))

        math = ((w * x1r) / 2) - (w * x1r * 0.5) / 2
        widgets["OPTS"].place(x=math,
                              y=(h * (y2r + y1r) +
                                 (h * (y3r / 2) - 10)) + (buf),
                              w=int(w * x1r * 0.5),
                              h=int(h * (y3r / 2) - 10))
        widgets["PREV"].place(x=math - buf - (w * x1r * 0.15),
                              y=(h * (y2r + y1r) +
                                 (h * (y3r / 2) - 10)) + (buf),
                              w=int(w * x1r * 0.15),
                              h=int(h * (y3r / 2) - 10))
        widgets["NEXT"].place(x=math + buf + (w * x1r * 0.5),
                              y=(h * (y2r + y1r) +
                                 (h * (y3r / 2) - 10)) + (buf),
                              w=int(w * x1r * 0.15),
                              h=int(h * (y3r / 2) - 10))

    elif CURRENT_PAGE == "OptionsPage":

        widgets["OPTS_LABEL"].place(x=0,
                                    y=0,
                                    w=w,
                                    h=h * 0.12)

        a = len(widgets["OPTS_BUTS"])
        for i in range(a):
            button = widgets["OPTS_BUTS"][i]
            label = widgets["OPTS_TEXTS"][i]
            y = 100 + (i * h // 8.5)
            f1 = opts_label_font[0], int(
                opts_label_font[1] * (w + h) / 2 * 0.0015 - w // 1000) - 1
            button.place(x=w * 0.05, y=y, w=w // 4, h=h // 12)
            label.config(bg=upper_bg, font=f1, fg='white')
            label.place(x=(w * 0.05) + (w // 4) + (15),
                        y=y, w=w // 1.6, h=h // 12)

        y = 100 + ((i + 1) * h // 8.5)
        widgets["OPTS_BACK"].place(
            x=w // 2 - (w // 3) // 2,
            y=y,
            w=w // 3,
            h=h // 12)


def main():
    os.chdir(user)
    load_spells_file()
    pages = [MainPage, OptionsPage]
    app = MainApp(pages)
    app.geometry("800x600")
    app.resizable(True, True)
    preset_window(app)
    app.style = ttk.Style()
    # app.style.theme_use("clam") --> can set theme
    app.style.configure('TButton', background=upper_bg)
    app.style.configure('TButton', foreground='black')

    # This is telling what to do if the 'x' button is presses, here saving

    app.mainloop()


def window(frame, button_text, label=""):
    popup_window = tk.Toplevel(frame)
    preset_window(popup_window)
    label = tk.Label(popup_window, text=label)
    label.config(bg=base_color, font=FONT, fg='white')
    label.pack()
    button = ttk.Button(popup_window, text=button_text,
                        command=lambda: popup_window.destroy())
    button.pack()
    center(popup_window)
    popup_window.focus()
    button.focus()
    return popup_window


def check_code(frame, password):
    try:
        password = make_code(password)
        return password
    except WeakCodeError:
        window(frame, "Close", "Code too weak.")
        return False
    except ValueError:
        window(frame, "Close", "Password in digits only")
        return False


def check_entered_code(password):
    password = int(password)
    with open('datfile.SDE') as file:
        data = file.read()
    data = decrypt(data, int(password))
    if data == ex_text:
        return True
    else:
        return False


def password_check(frame, password):
    temp_text = ('Unable to check passcode\n'
                 + '             Might corrupt data\n'
                 + 'Suggestion : close program unless sure of passcode')
    try:
        open("datfile.SDE")
    except FileNotFoundError:
        window(frame, "Continue", label=temp_text)
        return True
    else:
        if not check_entered_code(password):
            window(frame, "Close", label="Wrong Password")
            return False

        else:
            return True


def log_in(frame, user_name, password):
    global code, user
    if not validate_values(frame, user_name, password):
        return None

    if check_user(user_name):
        user_name = make_folder_name(user_name)
        with FolderManager(user_name):
            # --- Check if the password is right ---
            if password_check(frame, password):
                code = password
                user = user_name
                frame.destroy()

            else:
                window(frame, "Close", "Wrong Password or UserName")
                return None

        main()

    else:
        window(frame, "Close", "User Does not Exist")


def sign_up(frame, user_name, password):
    global code, user
    if not validate_values(frame, user_name, password):
        return None

    if check_user(user_name):
        window(frame, "Close", "User already exists")
        return None

    else:
        user_name = make_folder_name(user_name)
        os.makedirs(user_name)
        with FolderManager(user_name):
            with open("datfile.SDE", 'w') as file:
                file.write(encrypt(ex_text, int(password)))

        window(frame, "Close", "User successfully created")
        time.sleep(2)
        user = user_name
        code = password
        frame.destroy()
        main()


def make_folder_name(user_name):
    return user_name + "-SDE"


def check_user(user_name):
    user_name = make_folder_name(user_name)
    return check_folder(user_name)


def validate_values(frame, user_name, password):
    password = check_code(frame, password)
    # The above function actually handles the complete password part
    if password is False:
        return False

    # folder name cant contain :
    # /\<>:*?"|
    invalid_chr = '/\\<>:*?"|'
    temp_text = 'User Name cant contain:\n' + " " * 15 + '/\\<>:*?" |'
    for i in invalid_chr:
        if i in user_name:
            window(frame, "Close",
                   label=temp_text)
            return False

    if len(user_name) < 4:
        window(frame, "Close", label="Too small UserName")
        return False
    if len(user_name) > 25:
        window(frame, "Close", label="Too big UserName")
        return False

    return True


def main_dir_check():
    if check_folder(main_folder):
        os.chdir(main_folder)
    else:
        os.makedirs(main_folder)
        os.chdir(main_folder)


def intro():
    os.chmod(os.getcwd(), 0o444)
    # --- host the intro intro_root ---
    intro_root = tk.Tk()
    intro_root.geometry("300x150")
    intro_root.resizable(False, False)
    preset_window(intro_root)

    intro_root.style = ttk.Style()
    # app.style.theme_use("clam") --> can set theme
    intro_root.style.configure('TButton', background=upper_bg)
    intro_root.style.configure('TButton', foreground='black')

    # --- Check and make the main directory ---
    main_dir_check()
    # ----

    code_var = tk.StringVar()
    user_var = tk.StringVar()

    label = tk.Label(intro_root, text="User:")
    label.config(bg=base_color, font=FONT, fg='white')
    label.place(x=15, y=25)
    user_box = tk.Entry(intro_root, textvariable=user_var)
    user_box.place(x=50 + 15, y=25, width=200, height=25)
    user_box.focus()

    label = tk.Label(intro_root, text="Code:")
    label.config(bg=base_color, font=FONT, fg='white')
    label.place(x=14, y=75)
    code_box = tk.Entry(intro_root, textvariable=code_var, show="*")
    code_box.place(x=50 + 15, y=75, width=200, height=25)

    log_in_b = ttk.Button(intro_root, text="Log In",
                          command=lambda: log_in(intro_root, user_var.get(),
                                                 (code_var.get())))
    log_in_b.place(x=25, y=115, w=100)

    sign_up_b = ttk.Button(intro_root, text="Sign up",
                           command=lambda: sign_up(intro_root, user_var.get(),
                                                   (code_var.get())))
    sign_up_b.place(x=300 - 25 - 100, y=115, w=100)

    intro_root.mainloop()


intro()
