class Subject(object):
    name: str
    code: str


class PastPaperWebsite:

    def __init__(self):
        self.__root_url = "https://"
        self.__level_subject_site = {
            "IGCSE": "",
            "AS & A-Level": "",
            "O Level": ""
        }

    def get_levels(self):
        pass

    def get_subjects(self, level):
        pass

    def get_papers(self, level, subject, season=None, year=None,
                   cata=None, paper_num=None, edition_num=None):
        pass


class GCEGuide(PastPaperWebsite):

    def __init__(self):
        super().__init__()
        self.__root_url = "https://papers.gceguide.com/"
        self.__level_subject_site = {
            "IGCSE": "IGCSE/",
            "AS & A-Level": "A%20Levels/",
            "O Level": "O%20Levels/"
        }


class PapaCambridge(PastPaperWebsite):

    def __init__(self):
        super().__init__()
        self.__root_url += "pastpapers.papacambridge.com/?dir=Cambridge%20International%20Examinations%20%28CIE%29"
        self.__level_subject_site = {
            "IGCSE": "IGCSE/",
            "AS & A-Level": "AS%20and%20A%20Level/",
            "O Level": "GCE%20International%20O%20Level/"
        }
