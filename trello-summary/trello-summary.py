import itertools
import datetime
import strict_rfc3339
import json
import sys
import textwrap
import argparse

def itercards(cards):
    for card in cards:
        ts = strict_rfc3339.rfc3339_to_timestamp(card['date'])
        dt = datetime.datetime.fromtimestamp(ts)
        card['date'] = dt
        yield card

def groupByDate(cards):
    def date_key(card):
        return card['date'].date()

    for date, cards in itertools.groupby(cards, date_key):
        yield date, cards

def groupById(cards):
    def id_key(card):
        return card['id']

    for date, cards in itertools.groupby(cards, id_key):
        yield date, cards

def sortByAttr(cards, attr):
    def cmpcard(a, b):
        return cmp(a[attr], b[attr])

    return sorted(cards, cmpcard)

def sortById(cards):
    return sortByAttr(cards, 'id')

def sortByDate(cards):
    return sortByAttr(cards, 'date')

def dateType(string):
    """
    Convert a date string to a date object
    """
    try:
        date = datetime.datetime.strptime(string, '%Y-%m-%d').date()
    except ValueError:
        msg = "%r is not a valid date" % string
        raise argparse.ArgumentTypeError(msg)
    return date

def filterDates(start, end, cards):
    def filt(item):
        if not start and not end:
            return True

        date = item['date'].date()
        if start and date < start:
            return False
        elif end and date > end:
            return False
        return True

    return itertools.ifilter(filt, cards)

def main():
    parser = argparse.ArgumentParser(description="""Summarise Trello activities by date. This reads JSON exported from Trello and
    processed by jq via standard input.""")
    parser.add_argument('-e', '--end-date', metavar='DATE', type=dateType, default=datetime.date.today(),
                       help='the date activities should end at, inclusive in the format YYYY-MM-DD')
    parser.add_argument('-s', '--start-date', metavar='DATE', type=dateType,
                       help='the date activities should start from, inclusive in the format YYYY-MM-DD')

    # Retrieve the arguments.
    args = parser.parse_args()

    # Sanity check the dates.
    if args.start_date and args.end_date and args.start_date > args.end_date:
        parser.exit(message="The start date cannot be after the end date")

    cards = filterDates(args.start_date, args.end_date, itercards(json.load(sys.stdin)))
    for date, day_cards in groupByDate(sortByDate(cards)):
        print "{:%a %d %b %Y}:".format(date)
        for id_, id_cards in groupById(sortById(list(day_cards))):
            card = next(id_cards)
            indent = "  [{0}]: ".format(card['project'])
            sindent = ' ' * (len(card['project']) + 6)
            print textwrap.fill(card['name'], width=80, initial_indent=indent, subsequent_indent=sindent)
        print

if __name__ == '__main__':
    main()
