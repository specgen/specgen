This is an experimental new codebase for specgen tools based on danbri's
specgen5 version (http://svn.foaf-project.org/foaftown/specgen/).

		heavily updated by Bob Ferris, July 2010
		<http://smiy.wordpress.com/author/zazi0815/>
		
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

example: specgen6.py --indir=onto/co/ --ns=http://purl.org/ontology/co/core# 
--prefix=co --ontofile=counterontology.owl --outdir=spec/co/ --templatedir=onto/co/ 
--outfile=counterontology.html

See libvocab.py and specgen6.py for details.

Status:

 - we load up and interpret the core RDFS/OWL 
 - we populate Vocab, Term (Class or Property) instances
 - able to generate a XHTML/RDFa ontology specification with common concepts and properties from OWL, RDFS, RDF

TODO:
 - enable more OWL features, especially an automated construction of owl:Ontology (currently this must be
   done manually in the template)
 - enable more support for other namespaces
 - restructure the code !!!


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
