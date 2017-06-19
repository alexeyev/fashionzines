import re
import urllib.request
import csv

from bs4 import BeautifulSoup

bs = BeautifulSoup()

LINK_PATTERN = re.compile("/magazines/[^/]+/$")
OUTLINK_PATTERN = re.compile("^http://www\.fashionmodeldirectory\.com/go-")


def get_links(letter, offset):
    url = "http://www.fashionmodeldirectory.com/magazines/search/alphabetical_order/" + letter + "/?start=" + str(
        offset)
    page = urllib.request.urlopen(url).read()
    bs = BeautifulSoup(page)
    newlinks = [e.attrs["href"] for e in bs.find_all(href=LINK_PATTERN)]
    return newlinks


def get_info_row(mlink):
    # todo: parse semi-structured data
    page = urllib.request.urlopen(mlink).read()
    bs = BeautifulSoup(page)
    name = [e.text for e in bs.find_all(itemprop="brand")][0]
    outlinks = "|".join([e.attrs["href"].replace('http://www.fashionmodeldirectory.com/go-', "") for e in
                         bs.find_all(href=OUTLINK_PATTERN)])
    info = " ".join([e.text for e in bs.find_all("div", {"class": "SubInfo"})]).replace("\n\n", '|').replace("\n", " ")
    print(info)

    return [mlink, outlinks, name, info]


with open("fmd_parsed_with_meta_2_QZ.tsv", "w+") as resultsfile:

    writer = csv.writer(resultsfile, delimiter="\t")

    for letter in "QRSTUVWXYZ":

        print(letter)

        count = 1000
        offset = 0
        links = []

        while count > 0:
            print(offset)

            try:
                newlinks = get_links(letter, offset)

                for mlink in newlinks:
                    try:
                        row = get_info_row(mlink)
                        writer.writerow(row)
                    except Exception as e:
                        print("PROBLEM OFFICER")
                        print(e.__traceback__)
                        print(e)
            except Exception as e:
                print("Can't get alpha page")
                print(e)

            count = len(newlinks)
            offset += 24
