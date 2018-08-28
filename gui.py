from crawler_core import *
from tkinter import *
from tkinter.filedialog import askdirectory
from ppwebsite import *

import multiprocessing as mul

info = {
    'database_location': 'Please select the folder-->',
}


criteria = {
    'year': [],
    'season': [],
    'index': [],
    'type': []

}

# Subject name in format <subject>_<code>
all_subjects_names = [
    'Economics_0455', 'Biology_0610', 'Geography_0460', 'History_0470', 'Mathematics_0580',
    'Physics_0625', 'English - Second Language (oral endorsement)_0510',
    'Computer Science_0478', 'Chemistry_0620', 'Drama_0411', 'Business Studies_0450'
]


using_website = GCEGuide()


def get_years(all_papers):
    all_years = []

    for paper in all_papers:
        if paper[6:8] not in all_years:
            all_years.append(paper[6:8])

    return all_years


class ListBoxPlus(Listbox):
    def __init__(self, master=None, cnf={}, **kw):
        self.contents = list()

        super().__init__(master, cnf, **kw)

    def insert(self, index, *elements):
        print(index, *elements)
        for e in elements:
            self.contents.append(e)

        super().insert(index, *elements)

    def delete(self, first, last=None):
        last_pos = len(self.contents) if last == END else last

        for count in range(first, last_pos):
            self.contents[count] = 'Deleting'

        count = 0
        while count < len(self.contents):
            if self.contents[count] == 'Deleting':
                self.contents.pop(count)
            else:
                count += 1

        super().delete(first, last)

    def clear(self):
        super().delete(0, END)

    def query(self, year=None, paper=None, type=None):
        self.clear()

        for p in self.contents:

            print(self.contents)

            if p is None:
                continue

            if year is not None and len(year) != 0:
                if p[5:8] not in year:
                    continue

            if paper is not None and len(paper) != 0:
                if p[12:14] not in paper:
                    continue

            if type is not None and len(type)!= 0:
                if p[9:11] not in type:
                    continue

            super().insert(END, p)




class MainWindow(Tk):

    def __init__(self):
        super().__init__()

        self.geometry('720x1080')

        self.__subject_selection = StringVar(self)  # variable to keep option menu selection
        self.__shown_papers = []  # variable to keep all shown papers in listbox

        # Row 1

        # subject option menu
        OptionMenu(
            self, self.__subject_selection, *all_subjects_names
        ).grid(row=1, column=1)

        # search all button
        Button(
            self, text='Search', command=self.__search_button_clicked
        ).grid(row=1, column=2)

        # Row 2

        # Row 3
        Label(
            self, text='Database Location:' + info['database_location'], name='database_loc'
        ).grid(row=3, column=1, sticky=W)

        Button(
            self, text='...', name='bt_ask_db_loc', command=self.__database_loc_button_clicked
        ).grid(row=3, column=2)

        # Row 4

        # Row 5
        ListBoxPlus(
            self, name='paper_shower', width=50, selectmode=MULTIPLE
        ).grid(row=5, column=1, rowspan=3)

        Button(
            self, text='Download All', state=DISABLED, name='bt_download_all',
            command=self.__download_all_button_clicked
        ).grid(row=5, column=2)

        # Row 6
        Button(
            self, text='Download Selected', state=DISABLED, name='bt_download_selected',
            command=self.__download_selected_button_clicked
        ).grid(row=6, column=2)

        # Row 7


        # Row 8
        Button(self, text='Enable Query', name='qry_enable',
               command=lambda: (self.fill_qry(qry), self.children['qry_enable'].destroy())).grid(row=8, column=1)

        # Row 9
        qry = Frame(self, name='qry')

        qry.grid(row=9, column=1)


        # Row 9

    def fill_qry(self, master):
        def start_search():
            self.children['paper_shower'].query(year=year_entry.get().split(','),
                                                type=type_entry.get().split(','),
                                                paper=paper_entry.get().split(','))


        Label(master, text='Enter year (s18). Seperate with comma. DO NOT TYPE SPACE.').grid(column=1)
        year_entry = Entry(master)
        year_entry.grid(column=1)

        Label(master, text='Enter type (qp, ms)').grid(column=1)
        type_entry = Entry(master)
        type_entry.grid(column=1)

        Label(master, text='Enter paper (31)').grid(column=1)
        paper_entry = Entry(master)
        paper_entry.grid(column=1)

        Button(text='start_search', command=start_search).grid(column=1)


    def __update_database_location(self):
        """
        Function which updates the download location.
        :return: <None>
        """

        new_location = askdirectory()

        info['database_location'] = new_location
        self.children['database_loc']['text'] = 'Database Location:' + new_location

    def __update_buttons(self):
        """
        Function that updates the button status. If an database location is given then the download buttons are enabled.
        :return: <None>
        """

        database_bt = self.children['bt_ask_db_loc']
        all_bt = self.children['bt_download_all']
        selected_bt = self.children['bt_download_selected']

        if info['database_location'] == 'Please select the folder-->' or not self.__shown_papers:
            database_bt.flash()
            all_bt['state'] = DISABLED
            selected_bt['state'] = DISABLED
        else:
            all_bt['state'] = ACTIVE
            selected_bt['state'] = ACTIVE

    def __update_paper_list(self):
        """
        Function that shows the past papers onto the list box.
        :param paper_str: <str> String contains subject and code from listbox, e.g. Economics_0455
        :return: <None>
        """

        paper_str = self.__subject_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]

        self.__shown_papers = search_all(subject, code)

        ps = self.children['paper_shower']
        ps.delete(0, END)  # Clear the listbox

        for paper in self.__shown_papers:
            ps.insert(END, paper)

    def __search_button_clicked(self):
        self.__update_paper_list()
        self.__update_buttons()

    def __database_loc_button_clicked(self):
        self.__update_database_location()
        self.__update_buttons()

    def __download_all_button_clicked(self):
        paper_str = self.__subject_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]
        to_path = info['database_location'] + '/'

        download_papers(subject, code, to_path, self.__shown_papers)

    def __get_selected_papers(self):
        paper_shower = self.children['paper_shower']
        selected_indices = paper_shower.curselection()
        for index in selected_indices:
            yield paper_shower.get(index)

    def __download_selected_button_clicked(self):
        paper_str = self.__subject_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]
        to_path = info['database_location'] + '/'

        download_papers(subject, code, to_path, self.__get_selected_papers())







def main():
    app = MainWindow()

    app.mainloop()


if __name__ == '__main__':
    main()
