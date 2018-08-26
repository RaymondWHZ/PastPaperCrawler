from crawler_core import *
from tkinter import *
from tkinter.filedialog import askdirectory

info = {
    'database_location': 'Please select the folder-->',
}

# Subject name in format <subject>_<code>
all_subjects_names = [
    'Economics_0455', 'Biology_0610', 'Geography_0460', 'History_0470', 'Mathematics_0580',
    'Physics_0625', 'English - Second Language (oral endorsement)_0510',
    'Computer Science_0478', 'Chemistry_0620', 'Drama_0411', 'Business Studies_0450'
]


class MainWindow(Tk):

    def __init__(self):
        super().__init__()

        self.geometry('1920x1080')

        # variable to keep option menu selection
        self.subject_selection = subject_selection = StringVar(self)

        # Row 1

        # subject option menu
        OptionMenu(
            self, subject_selection, *all_subjects_names
        ).grid(row=1, column=1)

        # search all button
        Button(
            self, text='Search', command=self.search_button_clicked
        ).grid(row=1, column=2)

        # Row 2

        # Row 3
        Label(
            self, text='Database Location:' + info['database_location'], name='database_loc'
        ).grid(row=3, column=1, sticky=W)

        Button(
            self, text='...', name='bt_ask_db_loc', command=self.database_loc_button_clicked
        ).grid(row=3, column=2)

        # Row 4

        # Row 5
        Listbox(
            self, name='paper_shower', width=50, selectmode=MULTIPLE
        ).grid(row=5, column=1, rowspan=3)

        Button(
            self, text='Download All', state=DISABLED, name='bt_download_all',
            command=self.download_all_button_clicked
        ).grid(row=5, column=2)

        # Row 6
        Button(
            self, text='Download Selected', state=DISABLED, name='bt_download_selected',
            command=self.download_selected_button_clicked
        ).grid(row=6, column=2)

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

        if info['database_location'] == 'Please select the folder-->':
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

        paper_str = self.subject_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]

        all_papers = search_all(subject, code)

        ps = self.children['paper_shower']
        ps.delete(0, END)  # Clear the listbox

        for paper in all_papers:
            ps.insert(END, paper)

    def search_button_clicked(self):
        self.__update_paper_list()
        self.__update_buttons()

    def database_loc_button_clicked(self):
        self.__update_database_location()
        self.__update_buttons()

    def download_all_button_clicked(self):
        paper_str = self.subject_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]
        to_path = info['database_location'] + '/'

        download_papers(subject, code, to_path)

    def download_selected_button_clicked(self):
        paper_str = self.subject_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]
        to_path = info['database_location'] + '/'

        paper_shower = self.children['paper_shower']
        selected_indices = paper_shower.curselection()

        def get_specified_papers():
            for index in selected_indices:
                yield paper_shower.get(index)

        download_papers(subject, code, to_path, get_specified_papers())


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
