import urllib.request as rq
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

forge_agent_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def read_url(url):
    i_rq = rq.Request(url=url, headers=forge_agent_header)
    return rq.urlopen(i_rq).read()


def download_file(url: str, to_path: str):
    if to_path.endswith('/'):
        to_path += '/'

    i_rq = rq.Request(url=url, headers=forge_agent_header)
    ret = rq.urlopen(i_rq).read()

    file_name = url[url.rfind('/') + 1:]
    with open(to_path + file_name, "wb") as f:
        f.write(ret)


def main():
    pass


if __name__ == '__main__':
    main()
