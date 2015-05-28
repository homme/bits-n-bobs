# Trello Summary

Summarise your activities on Trello by date.

## Usage

Use [jq](http://stedolan.github.io/jq/) to format Trello JSON exports into the
appropriate structure:

```
jq --slurp '[.[] | .actions | .[] | select(.memberCreator.username == "homme") | {name: .data.card.name, date: .date, project: .data.board.name, id: .data.card.id} | select(.name != null)]' ./trello-exports/*.json | \
python2 trello-summary.py --start-date 2015-05-01 -end-date 2015-05-31
```

You'll probably want to change or remove the jq username filter. The date
filters are optional.
