import urllib.request as rq
from bs4 import BeautifulSoup


gce_guide_root_url = "https://papers.gceguide.com/IGCSE/"
forge_agent_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def search_with_specified_url(specified_url):
    i_rq = rq.Request(url=specified_url, headers=forge_agent_header)
    ret = rq.urlopen(i_rq).read()
    html_phrase = BeautifulSoup(ret, 'lxml')

    papers = html_phrase.select('#ggTable > tbody > tr > td > a')

    all_papers = []
    for p in papers:
        all_papers.append(p['href'])

    return all_papers


def search_all(subject, code):
    specified_url = gce_guide_root_url + subject + "%20(" + code + ")/"
    return search_with_specified_url(specified_url)


def download_all(subject, code, to_path):
    specified_url = gce_guide_root_url + subject + "%20(" + code + ")/"

    for paper in search_with_specified_url(specified_url):
        i_rq = rq.Request(url=specified_url+paper, headers=forge_agent_header)
        ret = rq.urlopen(i_rq).read()
        with open(to_path + paper, "wb") as f:
            f.write(ret)


def main():
    print(search_all("Economics", "0455"))
    download_all("Economics", "0455", "/Users/wuhaozhen/Downloads/Economics/")


def test():
    pass
    pass

if __name__ == '__main__':
    main()
