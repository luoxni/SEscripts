#!/usr/bin/python

import json
from json import JSONDecoder
import os
import math
import sys,getopt
import pprint
import re

## Rules for masking
## By default string values are turned into an equally long string of 'x'
## Integers are turned into an int of equal digits but all 9s
## Floats also turned into 9s.
## Booleans are ints underneath, all turned into 1s
def applyMask(value):
   if isinstance(value, basestring):
      length=len(value)
      masked='x' * length
      return masked
   if isinstance(value, int):
      if value > 1:
         digits = int(math.log10(value))+1
         masked='9' * digits
         return int(masked)
      elif value == 0 or value ==1:
         return "1"
      else:
         digits = int(math.log10(-value))+1
         masked='9' * digits
         return int(masked)
   if isinstance(value, float):
      newVal=re.sub(r'[0-9]',"9",str(value))
      return float(newVal)


## Iterate through nested structure, prints keys as they are being evaluated
## Handles nested objects and dicts
def iterate(dictionary, path=[]):
   for key, value in dictionary.items():
      try:
         key
      except:
         continue
      print path + [key]
      if isinstance(value, dict):
         iterate(value, path + [key])
         continue
      elif isinstance(value, list):
            for val in value:
                if isinstance(val, basestring):
                    newVal=applyMask(val)
                    dictionary[key]=newVal
                elif isinstance(val, list):
                    continue
                else:
                    iterate(val, path + [key])
      newVal=applyMask(value)
      dictionary[key]=newVal
      #print('key : {!r} -> value : {!r}'.format(path+[key], newVal))

## Code to find positions of stacked JSON objects
def decode_stacked(document, pos=0, decoder=JSONDecoder()):
   NOT_WHITESPACE = re.compile(r'[^\s]')
   while True:
      match = NOT_WHITESPACE.search(document, pos)
      if not match:
         return
      pos = match.start()

      try:
         obj, pos = decoder.raw_decode(document, pos)
      except JSONDecodeError:
         # do something sensible if there's some error
         raise "Error: Cannot find valid JSON position"
      yield obj


def main(argv):

   pp = pprint.PrettyPrinter(indent=2)
  
   # Read command line arguments
   inf = ''
   outf = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'maskJson.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inf = arg
      elif opt in ("-o", "--ofile"):
         outf = arg


   print 'Input file is ', inf

   # Open file and flatten into string
   with open(inf, 'r') as file:
      data = file.read().replace('\n', '')

   outdata=""

   # For files with stacked JSON, read each JSON object and parse individually
   for obj in decode_stacked(data):
      newjson=obj
      #pp.pprint(newjson)
      
      iterate(newjson)

      #pp.pprint(newjson)
      outdata+=json.dumps(newjson)+"\n"

   f = open(outf, "w")
   f.write(outdata)
   f.close()

if __name__ == "__main__":
   main(sys.argv[1:])
