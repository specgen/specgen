SpecGen v6
==========

About
-----

This is an experimental new codebase for [specgen](http://forge.morfeo-project.org/wiki_en/index.php/SpecGen) tools based on danbri's [specgen5 version](http://svn.foaf-project.org/foaftown/specgen/), 
which was heavily updated by [Bo Ferri](http://github.com/zazi/) in summer 2010.

<b>Features (incl. modifications + extensions)</b>:

* multiple property and class types
* muttiple restrictions modelling
* rdfs:label, rdfs:comment
* classes and properties from other namespaces
* inverse properties (explicit and anonymous)
* sub properties
* union ranges and domains (appear only in the property descriptions, not on the class descriptions)
* equivalent properties
* simple individuals as optional feature

Dependencies
------------
		
It depends utterly upon 

* [rdflib](http://rdflib.net/)
* [rdfextras](http://code.google.com/p/rdfextras/)
* [pyparsing](http://pyparsing.wikispaces.com/) (`easy_install pyparsing`)
	
(at least I had to install these packages additionally ;) )

If you're lucky, typing this is enough:

	easy_install rdflib

and if you have problems there, update easy_install etc with:

	easy_install -U setuptools
	
Purpose
-------
	
<b>Inputs</b>: [RDF](http://www.w3.org/TR/rdf-primer/), HTML and [OWL](http://www.w3.org/TR/owl-semantics/) description(s) of an RDF vocabulary<br/>
<b>Output</b>: an [XHTML+RDFa](http://www.w3.org/TR/rdfa-syntax/) specification designed for human users

Example
-------

	specgen6.py --indir=onto/olo/ --ns=http://purl.org/ontology/olo/core#  --prefix=olo --ontofile=orderedlistontology.owl --outdir=spec/olo/ --templatedir=onto/olo/ --outfile=orderedlistontology.html

* the template of this example can also be found in the folder: onto/olo
* the output of this example can also be found in the folder: spec/olo

See [libvocab.py](https://github.com/zazi/specgen/blob/master/libvocab.py) and [specgen6.py](https://github.com/zazi/specgen/blob/master/specgen6.py) for details.

Status
------

* we load up and interpret the core RDFS/OWL 
* we populate Vocab, Term (Class, Property or Individual) instances
* able to generate a XHTML/RDFa ontology specification with common concepts and properties from OWL, [RDFS](http://www.w3.org/TR/rdf-schema/), RDF

PS
--

The [old project repository location at SourceForge](http://smiy.svn.sourceforge.net/viewvc/smiy/specgen/) is now deprecated. All new developments will be pushed to this repository location here at GitHub.