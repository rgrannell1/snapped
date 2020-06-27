package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"

	"github.com/docopt/docopt-go"
)

func enumerateProperties(names []string, data interface{}) ([]string, error) {
	switch typeVal := data.(type) {
	case map[string]interface{}:
		// -- enumerate down & track property names.
		for key, _ := range typeVal {
			names = append(names, key)
		}
	default:
		return nil, errors.New("did not match type")
	}

	return names, nil
}

func analyseIndex(arguments docopt.Opts) error {
	fpath, _ := arguments.String("<index>")

	plan, _ := ioutil.ReadFile(fpath)
	var data interface{}
	err := json.Unmarshal(plan, &data)

	if err != nil {
		return errors.New("SNP_001" + ": failed to parse JSON data")
	}

	switch typed := data.(type) {
	case map[string]interface{}:
		var names []string
		names, _ = enumerateProperties(names, typed["mappings"])

		fmt.Println(names)
	default:
		return errors.New("SNP_001" + ": failed to parse JSON data mappings")
	}

	return nil
}

func main() {
	usage := `Tools you wish ElasticSearch shipped with.

Usage:
  snapped analyseIndex <index>
	snapped -h | --help
	snapped --version

Description:
	snapped automates several minor but time-consuming ElasticSearch maintanance tasks.

Analyse:
	This command analyses the field-names in an index mapping to help cut down the number of fields selectively.

Options:
  -h --help     Show this screen.
	--version     Show version.

Copyright:
  The MIT License
  Copyright (c) 2020 Róisín Grannell
  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify, merge,
  publish, distribute, sublicense, and/or sell copies of the Software, and to permit
  persons to whom the Software is furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all copies
  or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
  OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
  OTHER DEALINGS IN THE SOFTWARE.`

	arguments, _ := docopt.ParseDoc(usage)

	if arguments["analyseIndex"] == true {
		err := analyseIndex(arguments)

		if err != nil {
			log.Fatal(err)
		}
	}
}
