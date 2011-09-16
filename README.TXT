This is an experimental new codebase for specgen tools based on danbri's
specgen5 version (http://svn.foaf-project.org/foaftown/specgen/).

		heavily updated by Bo Ferri, July 2010
		<http://github.com/zazi/>
		
It depends utterly upon rdflib. See http://rdflib.net/
		+ http://code.google.com/p/rdfextras/
		+ http://pyparsing.wikispaces.com/ (easy_install pyparsing)
		(at I had to install these packages additionally ;) )

If you're lucky, typing this is enough: 
					easy_install rdflib

and if you have problems there, update easy_install etc with: 

					easy_install -U setuptools

Inputs: RDF, HTML and OWL description(s) of an RDF vocabulary
Output: an XHTML+RDFa specification designed for human users

example: specgen6.py --indir=onto/olo/ --ns=http://purl.org/ontology/olo/core# 
--prefix=olo --ontofile=orderedlistontology.owl --outdir=spec/olo/ --templatedir=onto/olo/ 
--outfile=orderedlistontology.html

-> the template of this example can also be found in the folder: onto/olo
-> the output of this example can also be found in the folder: spec/olo

See libvocab.py and specgen6.py for details.

Status:

 - we load up and interpret the core RDFS/OWL 
 - we populate Vocab, Term (Class, Property or Individual) instances
 - able to generate a XHTML/RDFa ontology specification with common concepts and properties from OWL, RDFS, RDF

TODO:
 - enable more OWL features, especially an automated construction of owl:Ontology (currently this must be
   done manually in the template)
 - enable more support for other namespaces (super classes and super properties from other namespaces already possible)
 - restructure the code !!!
 - write a cool parser for the "\n"'s and "\t"'s etc. in the parsed comments (e.g. "\n" to <br/> ...)


ISSUES

1. librdf doesn't seem to like abbreviations in FILTER clauses.
this worked:

q= 'SELECT ?x ?l ?c ?type WHERE { ?x rdfs:label ?l . ?x rdfs:comment ?c . ?x a ?type .  FILTER (?type = <http://www.w3.org/2002/07/owl#ObjectProperty>)  } '

while this failed:

q= 'PREFIX owl: <http://www.w3.org/2002/07/owl#> SELECT ?x ?l ?c ?type WHERE { ?x rdfs:label ?l . ?x rdfs:comment ?c . ?x a ?type .  FILTER (?type = owl:ObjectProperty)  } '

(even when passing in bindings)

This forces us to be verbose, ie.
q= 'SELECT distinct ?x ?l ?c WHERE { ?x rdfs:label ?l . ?x rdfs:comment ?c . ?x a ?type . FILTER (?type = <http://www.w3.org/2002/07/owl#ObjectProperty> || ?type = <http://www.w3.org/2002/07/owl#DatatypeProperty> || ?type = <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> || ?type = <http://www.w3.org/2002/07/owl#FunctionalProperty> || ?type = <http://www.w3.org/2002/07/owl#InverseFunctionalProperty>) } '

2. TODO: work out how to do ".encode('UTF-8')" everywhere

3. Be more explicit and careful re defaulting to English, and more robust when
multilingual labels are found.


PS: The old project repository location at SourceForge (http://smiy.svn.sourceforge.net/viewvc/smiy/specgen/) is now deprecated. All new developments will pushed to this repository location here at GitHub.