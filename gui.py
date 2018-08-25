from crawler_core import *
from tkinter import *
from tkinter.filedialog import *

info = {
    'database_location': 'Please select the folder-->',

}


def ui_make_app():
    '''
    Function that initialized the GUI interface.
    :return: <Tk> The GUI Interface
    '''
    app = Tk()
    app.geometry('1920x1080')

    sub_selection = StringVar(app)
    all_subjects_name = ['Economics_0455', 'Biology_0610']
    # Subject name in format <subject>_<code>

    # Row 1
    OptionMenu(app, sub_selection, *all_subjects_name).grid(row=1, column=1)
    Button(app, text='Search', command=lambda: ui_update_papers(sub_selection.get())).grid(row=1, column=2)

    # Row 2

    # Row 3
    Label(app, text='Database Location:'+info['database_location'], name='database_loc').grid(row=3, column=1, sticky=W)
    Button(app, text='...', command=__update_database_location).grid(row=3, column=2)

    # Row 4

    # Row 5
    Listbox(app, name='paper_shower', width=50, selectmode=MULTIPLE).grid(row=5, column=1, rowspan=3)
    Button(app, text='Download All', state=DISABLED, command=lambda: download_all(
        sub_selection.get().split('_')[0], sub_selection.get().split('_')[1], info['database_location']+'/')
           )\
        .grid(row=5, column=2)

    # Row 6
    Button(app, text='Download Selected',  command=lambda: download_papers(
        sub_selection.get().split('_')[0], sub_selection.get().split('_')[1], info['database_location'] + '/', app.children['paper_shower'])
           ).grid(row=6, column=2)



    return app


def __update_database_location():
    '''
    Function which updates the download location.
    :return: <None>
    '''
    new_location = askdirectory()

    info['database_location'] = new_location
    app.children['database_loc']['text'] = 'Database Location:' + info['database_location']







def ui_update_papers(paper_str):
    '''
    Function that shows the past papers onto the list box.
    :param paper_str: <str> String contains subject and code from listbox, e.g. Economics_0455
    :return: <None>
    '''
    code = paper_str.split('_')[1]
    name = paper_str.split('_')[0]

    all_papers = search_all(name, code)

    ps = app.children['paper_shower']
    ps.delete(0, END)   # Clear the listbox

    for paper in all_papers:
        ps.insert(END, paper)


def main():
    '''
    MAIN.
    :return: <None>
    '''
    global app
    app = ui_make_app()
    app.mainloop()


if __name__ == '__main__':
    main()