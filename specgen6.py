#!/usr/bin/env python

# This is a draft rewrite of specgen5, the family of scripts (originally
# in Ruby, then Python) that are used with the Counter Ontology, Ordered Lists
# Ontology and Info Service Ontology.
# This version is based on danbri's specgen version (specgen5) and heavily extended
# by Bob Ferris in July 2010 (the main extensions are in libvocab.py). This version is
# a bit more FOAF independent ;)
#
# spegen6:
#
#   Copyright 2010 Bob Ferris <http://smiy.wordpress.com/author/zazi0815/>
#
# specgen5:
#
# 	Copyright 2008 Dan Brickley <http://danbri.org/>
#
# ...and probably includes bits of code that are:
#
# 	Copyright 2008 Uldis Bojars <captsolo@gmail.com>
# 	Copyright 2008 Christopher Schmidt
#
# This software is licensed under the terms of the MIT License.
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



import libvocab
from libvocab import Vocab, VocabReport
from libvocab import Term
from libvocab import Class
from libvocab import Property
import sys
import os.path
import getopt


# Make a spec
def makeSpec(indir, uri, shortName,outdir,outfile, template, templatedir,indexrdfdir, ontofile):
  spec = Vocab( indexrdfdir, ontofile, uri)
  spec.addShortName(shortName)
  spec.index() # slurp info from sources

  out = VocabReport( spec, indir, template, templatedir ) 

  filename = os.path.join(outdir, outfile)
  print "Printing to ",filename

  f = open(filename,"w")
  result = out.generate()
  f.write(result)

# Make FOAF spec
def makeFoaf():
  makeSpec("examples/foaf/","http://xmlns.com/foaf/0.1/","foaf","examples/foaf/","_tmp_spec.html","template.html","examples/foaf/","examples/foaf/")


def usage():
  print "Usage:",sys.argv[0],"--indir=dir --ns=uri --prefix=prefix [--outdir=outdir] [--outfile=outfile] [--templatedir=templatedir] [--indexrdf=indexrdf] [--ontofile=ontofile]"
  print "e.g. "
  print sys.argv[0], " --indir=examples/foaf/ --ns=http://xmlns.com/foaf/0.1/ --prefix=foaf --ontofile=index.rdf"
  print "or "
  print sys.argv[0], " --indir=../../xmlns.com/htdocs/foaf/ --ns=http://xmlns.com/foaf/0.1/ --prefix=foaf --ontofile=index.rdf --templatedir=../../xmlns.com/htdocs/foaf/spec/ --indexrdfdir=../../xmlns.com/htdocs/foaf/spec/ --outdir=../../xmlns.com/htdocs/foaf/spec/"

def main():
  ##looking for outdir, outfile, indir, namespace, shortns

  try:
        opts, args = getopt.getopt(sys.argv[1:], None, ["outdir=", "outfile=", "indir=", "ns=", "prefix=", "templatedir=", "indexrdfdir=", "ontofile="])
        #print opts
  except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print "something went wrong"
        usage()
        sys.exit(2)

  indir = None #indir
  uri = None #ns
  shortName = None #prefix
  outdir = None 
  outfile = None
  templatedir = None
  indexrdfdir = None
  ontofile = None

  if len(opts) ==0:
      print "No arguments found"
      usage()
      sys.exit(2)   
  

  for o, a in opts:
      if o == "--indir":
            indir = a
      elif o == "--ns":
            uri = a
      elif o == "--prefix":
            shortName = a
      elif o == "--outdir":
            outdir = a
      elif o == "--outfile":
            outfile = a
      elif o == "--templatedir":
            templatedir = a
      elif o == "--indexrdfdir":
            indexrdfdir = a
      elif o == "--ontofile":
      		ontofile = a

#first check all the essentials are there

  # check we have been given a indir
  if indir == None or len(indir) ==0:
      print "No in directory given"
      usage()
      sys.exit(2)   

  # check we have been given a namespace url
  if (uri == None or len(uri)==0):
      print "No namespace uri given"
      usage()
      sys.exit(2)   

  # check we have a prefix
  if (shortName == None or len(shortName)==0):
      print "No prefix given"
      usage()
      sys.exit(2)
      
  # check we have benn given an ontology file
  if (ontofile == None or len(ontofile)==0):
  	print "No ontology file given"
        usage()
        sys.exit(2)
  else:
  	print "Use ontology file ",ontofile    

  # check outdir
  if (outdir == None or len(outdir)==0):
      outdir = indir
      print "No outdir, using indir ",indir
  
  if (outfile == None or len(outfile)==0):
      outfile = "_tmp_spec.html"
      print "No outfile, using ",outfile

  if (templatedir == None or len(templatedir)==0):
      templatedir = indir
      print "No templatedir, using ",templatedir

  if (indexrdfdir == None or len(indexrdfdir)==0):
      indexrdfdir = indir
      print "No indexrdfdir, using ",indexrdfdir

# now do some more checking
  # check indir is a dir and it is readable and writeable
  if (os.path.isdir(indir)):
      print "In directory is ok ",indir
  else:
      print indir,"is not a directory"
      usage()
      sys.exit(2)   


  # check templatedir is a dir and it is readable and writeable
  if (os.path.isdir(templatedir)):
      print "Template directory is ok ",templatedir
  else:
      print templatedir,"is not a directory"
      usage()
      sys.exit(2)   


  # check indexrdfdir is a dir and it is readable and writeable
  if (os.path.isdir(indexrdfdir)):
      print "indexrdfdir directory is ok ",indexrdfdir
  else:
      print indexrdfdir,"is not a directory"
      usage()
      sys.exit(2)   

  # check outdir is a dir and it is readable and writeable
  if (os.path.isdir(outdir)):
      print "Out directory is ok ",outdir
  else:
      print outdir,"is not a directory"
      usage()
      sys.exit(2)   

  #check we can read infile    
  try:
    filename = os.path.join(indexrdfdir, ontofile)
    f = open(filename, "r")
  except:
    print "Can't open ",ontofile,"  in ",indexrdfdir
    usage()
    sys.exit(2)   

  #look for the template file
  try:
    filename = os.path.join(templatedir, "template.html")
    f = open(filename, "r")
  except:
    print "No template.html in ",templatedir
    usage()
    sys.exit(2)   

  # check we can write to outfile
  try:
    filename = os.path.join(outdir, outfile)
    f = open(filename, "w")
  except:
    print "Cannot write to ",outfile," in",outdir
    usage()
    sys.exit(2)   

  makeSpec(indir,uri,shortName,outdir,outfile,"template.html",templatedir,indexrdfdir, ontofile)
  

if __name__ == "__main__":
    main()

