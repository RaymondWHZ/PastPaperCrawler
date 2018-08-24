from crawler_core import *
from tkinter import *

def make_app():
    app = Tk()
    app.geometry('1920x1080')



    sub_selection = StringVar(app)
    all_subjects_name = ['Economics_0455']

    OptionMenu(app, sub_selection, *all_subjects_name, width=50).grid(row=1, column=1)
    Button(app, text='Search').grid(row=1, column=2)



    return app




def main():
    app = make_app()
    app.mainloop()


if __name__ == '__main__':
    main()