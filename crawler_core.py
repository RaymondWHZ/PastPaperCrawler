import urllib.request as rq
from bs4 import BeautifulSoup
import ssl
import re


ssl._create_default_https_context = ssl._create_unverified_context


gce_guide_root_url = "https://papers.gceguide.com/IGCSE/"
forge_agent_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def __gce_guide_specified_link(subject, code):
    return gce_guide_root_url + subject + "%20(" + code + ")/"


def __search_with_specified_url(specified_url):
    i_rq = rq.Request(url=specified_url, headers=forge_agent_header)
    ret = rq.urlopen(i_rq).read()
    html_phrase = BeautifulSoup(ret, 'lxml')

    paper_icons = html_phrase.select('#ggTable > tbody > tr > td > a')
    for paper_icon in paper_icons:
        yield paper_icon['href']


def search_all(subject, code):
    specified_url = __gce_guide_specified_link(subject, code)
    return list(__search_with_specified_url(specified_url))


def download_all(subject, code, to_path):
    specified_url = __gce_guide_specified_link(subject, code)

    for paper in __search_with_specified_url(specified_url):
        if not re.findall(r'\d{4}_[swy]\d{2}_\w{2}_[1234][123].pdf', paper):
            # If the paper is not a) past paper b) answer c) Future questions, then skip it.
            continue

        i_rq = rq.Request(url=specified_url+paper, headers=forge_agent_header)
        ret = rq.urlopen(i_rq).read()

        with open(to_path + paper, "wb") as f:
            f.write(ret)




def main():
    print(search_all("Economics", "0455"))
    download_all("Economics", "0455", "/Users/wuhaozhen/Downloads/Economics/")


if __name__ == '__main__':
    main()
