
import os
import json
from os import initgroups

constants = {
  "BAD_FILE": "SNP_001"
}

def analyseProperties2(ancestor, val):
  if isinstance(val, dict) and "properties" in val:
    decendents = []
    for key, innerVal in val["properties"].items():
      inner = analyseProperties2(ancestor + [key], innerVal)

      if isinstance(inner, list) and len(inner) > 0 and isinstance(inner[0], list):
        for entry in inner:
          decendents.append(entry)
      else:
        decendents.append(inner)
    return decendents
  elif isinstance(val, dict) and val["type"] == "text" and "fields" in val:
    return [
      ancestor,
      ancestor[0:-1] + [ancestor[-1] + '_keyword']
    ]
  else:
    return ancestor

def printIndexSummary (val, args):
  message = "".rjust(args["indent"], " ")
  message += ".".join(args["props"])

  if isinstance(val, dict) and "hackForBadProp" in val:

    if val["hackForBadProp"] > 1:
      percentage = 100 * (val["hackForBadProp"] / args["total"])
      print(message.ljust(40, " ") +
            str(val["hackForBadProp"]).ljust(10) + str(round(percentage)))
    else:
      print(message)

  if isinstance(val, dict):
    for prop, data in val.items():
      if prop == "hackForBadProp":
        continue
      printIndexSummary(data, {
        "props": args["props"] + [prop],
        "indent": args["indent"] + 2,
        "total": args["total"]
      })
  else:
    pass

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
      indexProps[index] = analyseProperties2([], mapping["mappings"])
    else:
      raise Exception(constants["BAD_FILE"] + ": " +
                      fpath + " had index " + index + " without mappings field.")

  state = { }

  for index, props in indexProps.items():
    for propList in props:
      present = state
      for propPart in propList:
        if propPart in present:
          present = present[propPart]
          present["hackForBadProp"] += 1
        else:
          present[propPart] = {
            "hackForBadProp": 1
          }
          present = present[propPart]

  print("property path".ljust(40) + "count".ljust(10) + "percentage")

  total = sum([entry["hackForBadProp"] for entry in state.values()])
  header = "total".ljust(40, ' ') + str(total).ljust(10) + str(100)
  print(header)

  printIndexSummary(state, {
    "indent": 0,
    "props": [],
    "total": total
  })
