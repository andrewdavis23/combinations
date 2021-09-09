from tkinter import *
from tkinter import filedialog
import pandas as pd

# INITIALIZE pancake emoji, final dataframe, file paths, upload file type
all_data = pd.DataFrame()
file_directs = []
file_list = ''

color_mode = 1

class theme():
    btn_font = 'bold'
    winbg = 'black'
    btn = 'orange'
    frm = 'gray15'
    txtfg = 'pink'
    txtbg = 'gray6'
    txt = '#44D62C' #neon green
    btntxt = '#4D4DFF' #neon blue
    btnbg = 'gray12'
    btnactbg = 'gray12'
    btnactfnt = '#FFAD00' #neon orange
    scrllbg = 'pink'

# select files and display file names in window
def open_file():
    global file_directs
    global file_list

    new_files = list(filedialog.askopenfilenames())
    file_directs.extend(new_files)

    # add filenames to the tk list box
    for i in new_files:
        fl = i.split('/')[-1] + '\n'
        file_list += fl
      
    txt_list.config(state=NORMAL, fg=theme.txtfg, bg=theme.txtbg, foreground=theme.txt)
    txt_list.delete('1.0', END)
    txt_list.insert(END, file_list)
    txt_list.config(state=DISABLED)

    # activate compile button
    check_ready()

def clear_files():
    global file_directs
    global file_list
    global all_data

    file_directs = []
    file_list = []
    all_data = pd.DataFrame()

    txt_list.config(state=NORMAL)
    txt_list.delete('1.0', END)
    txt_list.config(state=DISABLED)

    check_ready()

def compile_csv():
    # plan: make it append on matching column names. exclude excess columns
    global file_directs
    global all_data
    msg = 'Compiled\n'   

    for f in file_directs:
        file_name = f.split('/')[-1]
        file_ext = file_name.split('.')[-1]

        if file_ext == 'txt' : 
            temp_df = pd.read_csv(f, delimiter='\t')
            s = temp_df.shape
            msg += '{}\n  {} rows    {} cols\n'.format(file_name,s[0],s[1])
        elif file_ext == 'xlsx' : 
            temp_df = pd.read_excel(f)
            s = temp_df.shape
            msg += '{}\n  {} rows    {} cols\n'.format(file_name,s[0],s[1])
        elif file_ext == 'csv' : 
            temp_df = pd.read_csv(f)
            s = temp_df.shape
            msg += '{}\n  {} rows    {} cols\n'.format(file_name,s[0],s[1])
        else: msg += '\nError reading {}\n   File extension not .txt, .xlsx or .csv'

        all_data = all_data.append(temp_df, ignore_index=True)
    
    ads = all_data.shape
    msg += 'Compilation\n   {} rows    {} cols\n'.format(ads[0],ads[1])

    check_ready()

    txt_list.config(state=NORMAL, fg=theme.txtfg, bg=theme.txtbg, foreground=theme.txt)
    txt_list.delete('1.0', END)
    txt_list.insert(END, msg)
    txt_list.config(state=DISABLED)

def check_ready():
    global file_directs
    global all_data

    if len(file_directs) > 0:
        btn_compile['state'] = NORMAL
        btn_clear['state'] = NORMAL
        if all_data.shape[0] > 0:
            btn_save['state'] = NORMAL
        else:
            btn_save['state'] = DISABLED

    else:
        btn_compile['state'] = DISABLED
        btn_clear['state'] = DISABLED
        btn_save['state'] = DISABLED

def save_file():
    global all_data

    out_path = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if out_path is None:
        return
    all_data.to_csv(out_path, index=False, line_terminator='\n', sep='\t')
    out_path.close()

# window
root = Tk()
root.title("CSV Compiler")
root.geometry('610x377')
root.configure(bg=theme.winbg)
root.attributes('-alpha', 0.90)

# frame
upper_frame = Frame(root, bg=theme.frm, bd=5)
upper_frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.2, anchor="n")

lower_frame = Frame(root, bg=theme.frm, bd=5)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor="n")

# objects
btn_open_file = Button(upper_frame, text="Select Files", command=open_file, bg=theme.btnbg, fg=theme.btntxt, font=theme.btn_font, activebackground=theme.btnactbg, activeforeground=theme.btnactfnt)
btn_open_file.pack(side='left', expand=True)

btn_compile = Button(upper_frame, text="Compile", state=DISABLED, command=compile_csv, bg=theme.btnbg, fg=theme.btntxt, font=theme.btn_font, activebackground=theme.btnactbg, activeforeground=theme.btnactfnt)
btn_compile.pack(side='left', expand=True)

btn_save = Button(upper_frame, text="Save", state=DISABLED, command=save_file, bg=theme.btnbg, fg=theme.btntxt, font=theme.btn_font, activebackground=theme.btnactbg, activeforeground=theme.btnactfnt)
btn_save.pack(side='left', expand=True)

btn_clear = Button(upper_frame, text="Clear Files", state=DISABLED, command=clear_files, bg=theme.btnbg, fg=theme.btntxt, font=theme.btn_font, activebackground=theme.btnactbg, activeforeground=theme.btnactfnt)
btn_clear.pack(side='left', expand=True)

txt_list = Text(lower_frame, bg=theme.txtbg)
txt_list.pack(expand=True, fill='both')

# scrollbars
hbar=Scrollbar(root, orient=HORIZONTAL, bg=theme.scrllbg)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=txt_list.xview)
vbar=Scrollbar(root, orient=VERTICAL, bg=theme.scrllbg)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=txt_list.yview)

root.mainloop()