# CSV Multiplier

Output the result of multiplying the string in the first column of a CSV file by
the the value in the second column.

E.g. assuming the following CSV as input:

    Nourmoutier,
    Bordeaux,3
    Toulouse,2
    Port Saint Louis,8

the script will output:

    Nourmoutier
    Bordeaux
    Bordeaux
    Bordeaux
    Toulouse
    Toulouse
    Port Saint Louis
    Port Saint Louis
    Port Saint Louis
    Port Saint Louis
    Port Saint Louis
    Port Saint Louis
    Port Saint Louis
    Port Saint Louis

The CSV input is read from standard input and output is written to standard
output.

The script is useful for generating input for the
[Word Cloud Generator](http://www.jasondavies.com/wordcloud/) when the generator
is used with the **One word per line** option.

## Usage

    cat example-input.csv | python2 csv-multiplier.py
