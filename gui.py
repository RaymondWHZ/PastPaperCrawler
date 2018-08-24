from crawler_core import *
from tkinter import *
from tkinter.filedialog import *

def ui_make_app():
    app = Tk()
    app.geometry('1920x1080')

    sub_selection = StringVar(app)
    all_subjects_name = ['Economics_0455', 'Biology_0610']

    OptionMenu(app, sub_selection, *all_subjects_name).grid(row=1, column=1)
    Button(app, text='Search', command=lambda: ui_update_papers(sub_selection.get())).grid(row=1, column=2)

    Listbox(app, name='paper_shower', width=50, selectmode=MULTIPLE).grid(row=2, column=1)
    Button(app, text='Download', command=lambda: download_all(
        sub_selection.get().split('_')[0], sub_selection.get().split('_')[1], askdirectory()+'/'))\
        .grid(row=2, column=2)

    return app

def ui_update_papers(paper_str):
    code = paper_str.split('_')[1]
    name = paper_str.split('_')[0]

    all_papers = search_all(name, code)

    ps = app.children['paper_shower']
    ps.delete(0, END)

    for paper in all_papers:
        ps.insert(END, paper)

    print(all_papers)


def main():
    global app
    app = ui_make_app()
    app.mainloop()


if __name__ == '__main__':
    main()