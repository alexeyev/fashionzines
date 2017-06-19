import editdistance
import csv

magsfile = open("magazines.tsv")
magsreader = csv.reader(magsfile, delimiter='\t', quotechar='"')

# sitesfile = open("sites.tsv")
# sitesreader = csv.reader(sitesfile, delimiter='\t', quotechar='"')
# name2site = {row[0].lower(): row[1] for row in sitesreader}

sitesfile = open("fmd_parsed_AZ.tsv")
sitesreader = csv.reader(sitesfile, delimiter='\t', quotechar='"')
name2site = {row[2].lower().replace("'", ""): row[1] for row in sitesreader}

print(name2site)


def find_argmin_dist(shname):
    min_diff = 1000
    diff = None
    best = None

    for name in name2site:
        diff = editdistance.eval(name, shname)
        if diff < min_diff:
            best = name
            min_diff = diff

    min_diff_sh = 1000
    diff_sh = None
    best_sh = None

    for name in name2site:
        name_shorter = name.split(" ")[0]
        diff_sh = editdistance.eval(name_shorter, shname)

        if diff_sh < min_diff_sh:
            best_sh = name
            min_diff_sh = diff_sh

    return best, min_diff, best_sh, min_diff_sh


with open("matches_levenshtein.tsv", "w+") as wf:

    writer = csv.writer(wf, delimiter="\t")

    # O(n**2)
    for row in magsreader:
        name_shortened = row[0]
        bestmatch, ed, bestmatch2, ed2 = find_argmin_dist(name_shortened)
        writer.writerow((row[0], bestmatch, name2site[bestmatch], str(ed), bestmatch2, name2site[bestmatch2], str(ed2)))
