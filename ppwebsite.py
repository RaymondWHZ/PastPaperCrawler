import crawler_core as cc
from bs4 import BeautifulSoup
import re


def is_paper(name: str):
    return len(re.findall(r'\d{4}_[swy]\d{2}_\w{2}_[1234][123].pdf', name)) == 1


class Subject(object):

    def __init__(self, name: str, code: str=None):
        """
        Call it in either way:

        1. Subject("Physics (0625)")
        2. Subject("Physics", "0625")

        Use str(subject) to get "Physics (0625)"
        """
        if code is None:
            sep = name.rfind('(')
            self.name = name[:sep - 1]
            self.code = name[sep + 1:sep + 5]
        else:
            self.name = name
            self.code = code

    def __str__(self):
        return self.name + " (" + self.code + ")"


class PastPaperWebsite(object):

    def __init__(self):
        self.__root_url = "https://"
        self.__level_site = {
            "IGCSE": "",
            "AS & A-Level": "",
            "O Level": ""
        }

    def get_subjects(self, level: str) -> iter:
        """
        Search for subjects.

        :param level: The level of the subject to search, one among "IGCSE", "AS & A-Level", "O Level".
        :return: Iterator that returns all subjects.
        """
        pass

    def get_papers(self, level: str, subject: Subject) -> iter:
        """
        Search for all papers.

        :param level: The level of the subject to search, one among "IGCSE", "AS & A-Level", "O Level".
        :param subject: The subject to search.
        :return: Iterator that returns all papers.
        """
        pass

    def download_papers(self, level: str, subject: Subject, specified_papers: list, to_path: str):
        """
        Function that downloads paper.

        :param level: The level of the subject to download, one among "IGCSE", "AS & A-Level", "O Level".
        :param subject: The subject to download.
        :param specified_papers: The specified papers to be downloaded
        :param to_path: The download path.
        """
        pass


class GCEGuide(PastPaperWebsite):

    def __init__(self):
        super().__init__()
        self.__root_url = "https://papers.gceguide.com/"
        self.__level_site = {
            "IGCSE": "IGCSE/",
            "AS & A-Level": "A%20Levels/",
            "O Level": "O%20Levels/"
        }

    @staticmethod
    def __subject_site(subject):
        return subject.name + "%20(" + subject.code + ")/"

    @staticmethod
    def __get_content_list(specified_url, criteria=lambda name: True):
        ret = cc.read_url(specified_url)
        html_phrase = BeautifulSoup(ret, 'lxml')

        file_icons = html_phrase.select('#ggTable > tbody > tr > td > a')
        for file_icon in file_icons:
            file = file_icon['href']
            if criteria(file):
                yield file

    def get_subjects(self, level):
        specified_url = self.__root_url + self.__level_site[level]
        return self.__get_content_list(specified_url, lambda name: name != "error_log")

    def get_papers(self, level, subject):
        specified_url = self.__root_url + self.__level_site[level] + self.__subject_site(subject)
        return self.__get_content_list(specified_url, is_paper)

    def download_papers(self, level, subject, specified_papers, to_path):
        specified_url = self.__root_url + self.__level_site[level] + self.__subject_site(subject)
        for paper in specified_papers:
            cc.download_file(specified_url + paper, to_path)


class PapaCambridge(PastPaperWebsite):

    def __init__(self):
        super().__init__()
        self.__root_url += "pastpapers.papacambridge.com/?dir=Cambridge%20International%20Examinations%20%28CIE%29"
        self.__level_subject_site = {
            "IGCSE": "IGCSE/",
            "AS & A-Level": "AS%20and%20A%20Level/",
            "O Level": "GCE%20International%20O%20Level/"
        }


def main():
    gce_guide = GCEGuide()
    gce_guide.download_papers("IGCSE", Subject("Physics (0625)"), ['0625_s14_ms_11.pdf', '0625_s14_ms_12.pdf', '0625_s14_ms_13.pdf'], '/Users/wuhaozhen/Downloads/Economics/')


if __name__ == '__main__':
    main()
