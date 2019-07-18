# SEscripts
Handy scripts for customer facing roles

## maskJson.py
Masks a JSON file while keeping the nested structure and file size. Handy for masking JSON files that contain private data. 

### Usage 
maskJson.py -i <inputfile> -o <outputfile>

###
Converts 
{"stringvalue":"examplestring"}
{"intvalue":12345}
{"floatvalue":123.456}
{"nestedkeys":{"boolean":true}}

to
{"stringvalue": "xxxxxxxxxxxxx"}
{"intvalue": 99999}
{"floatvalue": 999.999}
{"nestedkeys": {"boolean": "1"}}
