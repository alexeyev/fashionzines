import editdistance
import csv

magsfile = open("magazines.tsv")
magsreader = csv.reader(magsfile, delimiter='\t', quotechar='"')

sitesfile = open("sites.tsv")
sitesreader = csv.reader(sitesfile, delimiter='\t', quotechar='"')

name2site = {row[0].lower(): row[1] for row in sitesreader}


def find_argmin_dist(shname):
    min_diff = 1000
    diff = None
    best = None

    for name in name2site:
        diff = editdistance.eval(name, shname)
        if diff < min_diff:
            best = name
            min_diff = diff

    return best, min_diff


with open("matches_levenshtein.tsv", "w+") as wf:

    writer = csv.writer(wf, delimiter="\t")

    # O(n**2)
    for row in magsreader:
        name_shortened = row[0]
        bestmatch, ed = find_argmin_dist(name_shortened)

        writer.writerow((row[0], bestmatch, name2site[bestmatch], str(ed)))
