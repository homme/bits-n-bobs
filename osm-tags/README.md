# OSM Tags

Read in an OpenStreetMap XML file and output a CSV file with some simple tag
data.

The aim is to provide a quick, simple view into the tags.  The XML is parsed as
a stream, not read entirely into memory, so it is possible to process very large
XML files.

The OSM XML file must be named `export.osm` and must be placed in the current
working directory.  The CSV is output to standard output.  The first two CSV
columns output are the Key name and the number of times the key appears in the
XML file.  The remainder of the columns are the unique values appearing in the
tag.

## Usage

    osm-tags

## Installation

    go get github.com/homme/bits-n-bobs/osm-tags
    go install github.com/homme/bits-n-bobs/osm-tags
