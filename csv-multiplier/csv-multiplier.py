import csv
import sys

tagreader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in tagreader:
    multiplier = row[1]
    if not multiplier: multiplier = 1
    for i in xrange(int(multiplier)):
        print row[0]
