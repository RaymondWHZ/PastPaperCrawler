from crawler_core import *
from tkinter import *
from tkinter.filedialog import askdirectory


class MainFrame(Tk):

    def __init__(self):
        super().__init__()

        self.geometry('1920x1080')  # reset size

        self.sub_selection = sub_selection = StringVar(self)  # variable that records option menu selection
        all_subjects_name = ['Economics_0455', 'Biology_0610']  # available choices

        # subject option box
        OptionMenu(self, sub_selection, *all_subjects_name).grid(row=1, column=1)

        # search button
        Button(self, text='Search', command=self.update_paper_list).grid(row=1, column=2)

        # paper list
        Listbox(self, name='paper_shower', width=50, selectmode=MULTIPLE).grid(row=2, column=1)

        # download button
        Button(self, text='Download', command=self.download_all).grid(row=2, column=2)

    def update_paper_list(self):
        paper_str = self.sub_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]

        all_papers = search_all(subject, code)

        ps = self.children['paper_shower']
        ps.delete(0, END)

        for paper in all_papers:
            ps.insert(END, paper)

    def download_all(self):
        paper_str = self.sub_selection.get()
        subject = paper_str.split('_')[0]
        code = paper_str.split('_')[1]

        target_dir = askdirectory() + "/"
        download_all(subject, code, target_dir)


def main():
    app = MainFrame()
    app.mainloop()


if __name__ == '__main__':
    main()
