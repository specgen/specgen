SpecGen v6
==========

About
-----

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


PS: The old project repository location at SourceForge (http://smiy.svn.sourceforge.net/viewvc/smiy/specgen/) is now deprecated. All new developments will be pushed to this repository location here at GitHub.