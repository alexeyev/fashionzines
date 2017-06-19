import re
import urllib.request
import csv

from bs4 import BeautifulSoup

bs = BeautifulSoup()


def get_links(letter, offset):
    url = "http://www.fashionmodeldirectory.com/magazines/search/alphabetical_order/" + letter + "/?start=" + str(
        offset)
    page = urllib.request.urlopen(url).read()
    bs = BeautifulSoup(page)
    newlinks = [e.attrs["href"] for e in bs.find_all(href=re.compile("/magazines/[^/]+/$"))]
    return newlinks


def get_info_row(mlink):
    # todo: parse semi-structured data
    page = urllib.request.urlopen(mlink).read()
    bs = BeautifulSoup(page)
    name = [e.text for e in bs.find_all(itemprop="brand")][0]
    outlinks = "|".join([e.attrs["href"].replace('http://www.fashionmodeldirectory.com/go-', "") for e in
                         bs.find_all(href=re.compile("^http://www\.fashionmodeldirectory\.com/go-"))])

    return [mlink, outlinks, name, ]


with open("fmd_parsed.tsv", "w+") as resultsfile:
    writer = csv.writer(resultsfile, delimiter="\t")

    for letter in "ABCDEFGHIJKLMNOP":

        print(letter)

        count = 1000
        offset = 0
        links = []

        while count > 0:
            print(offset)
            newlinks = get_links(letter, offset)

            for mlink in newlinks:
                row = get_info_row(mlink)
                writer.writerow(row)

            count = len(newlinks)
            offset += 24

