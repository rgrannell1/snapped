
import os
import json

constants = {
  "BAD_FILE": "SNP_001"
}

def analyseProperties (props, mappings):
  if "properties" in mappings:
    for prop_name, prop_val in mappings["properties"].items():
      inner_props = analyseProperties({}, prop_val)
      props[prop_name] = inner_props
  else:
    is_text = "type" in mappings and mappings["type"] == "text"

    if not is_text:
      return

    has_keywords = "fields" in mappings and "keyword" in mappings["fields"]

    if not has_keywords:
      return

    has_keyword_type = "type" in mappings["fields"]["keyword"] and mappings["fields"]["keyword"]["type"] == "keyword"

    if not has_keyword_type:
      return

    return {
      "keyword": {}
    }

  return props

def snapped (raw_args):
  fpath = raw_args["<index>"]
  is_file = os.path.isfile(raw_args["<index>"])

  if not is_file:
    raise Exception(constants["BAD_FILE"] + ": " + fpath + " does not exist or was not a file.")

  try:
    with open(fpath, "r") as read_file:
      index_data = json.load(read_file)
  except:
    raise Exception(constants["BAD_FILE"] + ": " +
                   fpath + " contained malformed JSON.")

  indexProps = { }

  for index, mapping in index_data.items():
    if "mappings" in mapping:
      props = {}
      analyseProperties(props, mapping["mappings"])
      indexProps[index] = props
    else:
      raise Exception(constants["BAD_FILE"] + ": " +
                      fpath + " had index " + index + " without mappings field.")

  print(indexProps)
