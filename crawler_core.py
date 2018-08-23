import urllib.request as rq


gce_guide_root_url = "https://papers.gceguide.com/IGCSE/Economics%20(0455)/0455_m15_ms_12.pdf"
forge_agent_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def main():
    i_rq = rq.Request(url=gce_guide_root_url, headers=forge_agent_header)
    ret = rq.urlopen(i_rq).read()
    with open("/Users/wuhaozhen/Downloads/test.pdf", "wb") as f:
        f.write(ret)


if __name__ == '__main__':
    main()
