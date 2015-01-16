package main

// adapted from <http://blog.davidsingleton.org/parsing-huge-xml-files-with-go/>

import (
	"encoding/csv"
	"encoding/xml"
	"io"
	"os"
	"strconv"
)

type valueCounts map[string]int

var keyCounts = make(map[string]valueCounts)

func GetTags(xmlFile io.Reader) {
	decoder := xml.NewDecoder(xmlFile)

	type Tag struct {
		Key   string `xml:"k,attr"`
		Value string `xml:"v,attr"`
	}

	for {
		// Read tokens from the XML document in a stream.
		t, _ := decoder.Token()
		if t == nil {
			break
		}
		// Inspect the type of the token just read.
		switch se := t.(type) {
		case xml.StartElement:
			// If we just read a StartElement token and its name is "tag"
			if se.Name.Local == "tag" {
				var t Tag
				// decode a whole chunk of following XML into the variable t
				// which is a Tag (see above)
				decoder.DecodeElement(&t, &se)

				// aggregate the key counts
				keyValues := keyCounts[t.Key]
				if keyValues == nil {
					keyValues = make(valueCounts)
					keyCounts[t.Key] = keyValues
				}
				keyValues[t.Value] += 1
			}
		}
	}
}

func OutputTagCount(csvWriter io.Writer) {
	writer := csv.NewWriter(csvWriter)
	writer.Write([]string{"Key", "Tag Count", "Values..."})

	for key, values := range keyCounts {

		valueNames := make([]string, 0, len(values)+1)
		keyCount := 0
		for value, valueCount := range values {
			valueNames = append(valueNames, value)
			keyCount += valueCount
		}

		valueNames = append([]string{key, strconv.Itoa(keyCount)}, valueNames...)

		err := writer.Write(valueNames)
		if err != nil {
			panic(err)
		}
	}
	writer.Flush()
}

func main() {
	f, err := os.Open("./export.osm")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	GetTags(f)
	OutputTagCount(os.Stdout)
}
