#
# Extension of specgen6 producing automatic groups of concepts of the ontology
#
# It uses the igraph library (http://igraph.sourceforge.net/) and so the python interface for igraph is needed.
#
# It uses the walktrap community algorithm
# Some weighting of the graph is implemented, that distinguish between the different types of edges, also a hierarchical weighting
# of the rdfs:subClassOf Edges is used. That means the weight of subClassOf Edges gets higher, the deeper its relative position is.
# Also some kind of scoring the count and size of group is implemented. "Good groupings" for human readers are one that have about 4 groups
# and not more than 9 concepts per group.
# For bigger ontologies some kind of filtering or other measures have to be implemented.
#
#
# Usage: just add --groups parameter behind the starting command to enable the grouping
# An Template with that uses groups and and css that created a nice laylout is required. 
# A base template can be found in the "template" folder.
#
# Copyright 2012 Mario Rothe mario.rothe@gmail.com
# It is permited to do whatever you want with this code. So copy, edit, extend and use it as you like.
#


from collections import Counter

from igraph import *
from libvocab import Vocab;
import rdflib
from rdflib.namespace import Namespace
from rdflib.term import BNode

from igraph import Graph

RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')

NSBLACKLIST = ["http://www.w3.org/1999/02/22-rdf-syntax-ns#",
               'http://www.w3.org/2000/01/rdf-schema#',
               'http://www.w3.org/2002/07/owl#',
               "http://www.w3.org/2001/XMLSchema#"]

borderGroups = 4
borderConcepts = 8.5
weightModularity = 1
weightGroups = 2
weightSize =2

edgeWeights = {
            'default':1,
            RDFS.subClassOf: 25.0,
            RDFS.subPropertyOf:20.0,
            RDFS.domain:10.0,
            RDFS.range:5.0,
            OWL.equivalentClass:50.0,
            OWL.disjointWith:1.0
    }


#subClass variables
baseline = 0.25
trange = 5
multi = 17

#util functions

def getStringForList(group,ns):
        label = "{ ";
        for uri in group:
            label = label + uri.replace(ns,"")+", ";
        label = label +"}";
        return label;
        
        
def getLocalNameFromURI(uri):
        return(getLocalNameFromString(str(uri)));
        
        
def getLocalNameFromString(suri):
        if "#" in suri:
            localname = suri[suri.rfind("#")+1:len(suri)];
            return localname;
        
        if "/" in suri:
            localname = suri[suri.rfind("/")+1:len(suri)];
            return localname;
        
        return suri;

def verteil(x,expected,varianz):
    #print("Varianz:",varianz)
    #print("a = X-4/1.5",(x-expected)/varianz)
    #print("b = a^2",math.pow(((x-expected)/varianz), 2))
    expo = (-math.pow(((x-expected)/varianz),2)/2)
    #print("c = -1/2*b: ",expo)
    result = math.exp(expo)
    #print("verteil: ",result)
    return result







class Grouping(object):
    

    
    
    def __init__(self, spec,ns):
        self.spec = spec;
        self.gen = UniqueIdGenerator();
        self.ns = ns;
        
        
        
    def createConceptGraph(self):

        def getSubClassEdgeWeight(edge,elist):
            
            def getPosToTop(elist,n,visited):
                for e in elist:
                    if not e['type'] == RDFS.subClassOf:
                        continue;
                    if (e['source'] == n) & (not n in visited):
                        visited.append(n);
                        return getPosToTop(elist,e['target'],visited) +1;
                return 0;
            
            def getPosToBottom(elist,n,visited):
                max = 0;
                for e in elist:
                    if not e['type'] == RDFS.subClassOf:
                        continue;
                if (e['target'] == n) & (not n in visited):
                    visited.append(n);
                    depth = getPosToBottom(elist, e['source'],visited)+1;
                    if (depth>max):
                        max = depth;
                return max
            
            
            posToTop = getPosToTop(elist,edge['target'],[])+1;
            posToBottom = getPosToBottom(elist,edge['source'],[]);
            height = posToTop+posToBottom;
            if (height == 1):
                relPosInHierachie = 0;
            else: 
                relPosInHierachie = float(posToTop) / float(height);
            abw = relPosInHierachie - baseline;
            abwNorm = abw*trange;
            res = multi*(math.atan(abwNorm) + math.pi/2);
            return res;

        def filter(subject,classlist):
            if isinstance(subject,BNode): return True;
            if (str(subject) in classlist): return True;
            for ns in NSBLACKLIST:
                if str(subject).startswith(ns):
                    return True;
            return False;
            

        graph = self.spec.graph

        classtypes = [RDFS.Class, OWL.Class]
        classlist = []
        classObj = []
        nlist=[];
        elist=[];
        
        #create nodes
        for onetype in classtypes:
            for classSub in  graph.subjects(predicate=RDF.type, object=onetype):
                #print("checking: " +str(classSub));
                if not filter(classSub, classlist):
                    uri = str(classSub);
                    classlist.append(uri);
                    classObj.append(classSub);
                    #print("adding node: "+ uri);
                    nlist.append({'node':classSub,'uri':uri,'name':self.gen[uri],'label':str(uri).replace(self.ns, ""),"type":"Class"});
                #else: print("filtered")
        #print classObj
        #if class != null create owl:Thing node
        thing = OWL.Thing
        uri = str(thing);
        classlist.append(uri);
        classObj.append(thing);
        nlist.append({'node':thing,'uri':uri,'name':self.gen[uri],'label':str(uri).replace("http://www.w3.org/2002/07/owl#", ""),"type":"ExternalClass"});
        
        
        #create edges
        for c in classObj:    
            if (c == OWL.Thing):
                continue;
            found = False;
            
            
            #build concept hierachy
            for obj in graph.objects(c,RDFS.subClassOf):
                if ( obj in classObj):
                    found = True;
                    #get source and target id
                    source = self.gen[str(c)];
                    target = self.gen[str(obj)];
                    elist.append({"type":RDFS.subClassOf,'source':source,'target':target,"proptype":"language"});
                
            #add link to owl:thing if top node    
            if not found:
                #print("add subclass link for level1 class " + str(c.uri));
                source = self.gen[str(c)];
                target = self.gen[str(OWL.Thing)];
                elist.append({"type":RDFS.subClassOf,'source':source,'target':target,"proptype":"language"});
                
        
        #add domain level edges
        for sub,obj in graph.subject_objects(RDFS.domain):
            #test if obj in classlist
            if (obj in classObj):
                prop = sub;
                for rObj in graph.objects(prop,RDFS.range):
                    if (rObj in classObj):
                        #add a edge
                        
                        dom = obj;
                        range = rObj;
                        source = self.gen[str(dom)];
                        target = self.gen[str(range)];
                        #print("Adding  edge from "+ str(dom.uri) + " to " + str(range.uri) + " with Prop: "+str(prop.uri));
                        
                        elist.append({"type":prop,'source':source,'target':target,"proptype":"domain"});
                    
        #add some other language level edges
        for sub,obj in graph.subject_objects(OWL.equivalentClass):
            if (sub in classObj) and (obj in classObj):
                source = self.gen[str(sub)];
                target = self.gen[str(obj)];
                elist.append({"type":OWL.equivalentClass,'source':source,'target':target,"proptype":"language"});
        for sub,obj in graph.subject_objects(OWL.disjointWith):
            if (sub in classObj) and (obj in classObj):
                source = self.gen[str(sub)];
                target = self.gen[str(obj)];
                elist.append({"type":OWL.disjointWith,'source':source,'target':target,"proptype":"language"});
        
        
                    
        #nodes and edges created
        #weighting them
        
        for edge in elist:
            if (edge['type'] == RDFS.subClassOf):
                weight = getSubClassEdgeWeight(edge,elist);
                edge['weight'] = weight;
            elif edge['proptype'] == 'domain':
                weight = (edgeWeights[RDFS.domain]+edgeWeights[RDFS.range])/2;
                edge['weight'] = weight;
            else:
                weight = edgeWeights[edge['type']]
                if weight == None: weight =1;
                edge['weight'] = weight;
                    
        
        #print nlist;
        #print elist;
        g = Graph.DictList(vertices= nlist , edges=elist, directed=True);
        return g,classObj
    
    
    

        
    
    
    ## Group Size Part
    
    
    def groupsCountScore(self,g,membership,border):   
        localmembers = [];
        for i in range(0,len(membership)):
            if g.vs[i]["type"] =="Class":
                localmembers.append(membership[i])
        
        count = len(list(set(localmembers)))
        #print("Groups:",count);

        if count <= 1:
            return 0;
        elif (count <= border):
            return 1;
        else:
            return verteil(count,border,1.5);
        

    def groupConceptCountScore(self,g,membership,border):
        localmembers = [];
        groupscores = {}
        for i in range(0,len(membership)):
            if g.vs[i]["type"] =="Class":
                localmembers.append(membership[i])
        countvec = Counter(localmembers)
        for group,count in countvec.items():
            if (count == 1):
                groupscores[group] = 0;
            elif (count <= border):
                groupscores[group] = 1;
            else:
                groupscores[group] = verteil(count,border,4);
        erg = 0.0
        for (group,score) in groupscores.items():
            add = countvec[group]*score/float(len(localmembers))
            erg = erg+ add
        return erg;
        

    
    
    
    def processWalktrap(self,g):

        sumweight = weightModularity+weightGroups+weightSize;
        
        dendro = g.community_walktrap(weights='weight');
        #plot(dendro);
        scores = [];
        for i in range(0,len(dendro.merges)):
            membership = community_to_membership(dendro.merges,g.vcount(),i);
            modScore = g.modularity(membership,weights='weight');
            groupCountScore = self.groupsCountScore(g,membership,borderGroups);
            groupConceptCountScore = self.groupConceptCountScore(g,membership,borderConcepts);
            score = (weightModularity*modScore+weightGroups*groupCountScore+weightSize*groupConceptCountScore)/sumweight;
            #print("modScore: ",modScore)
            #print("groupCountScore: ",groupCountScore)
            #print("groupConceptCountScore:",groupConceptCountScore)
            #print("score: ",score);
            scores.append(score);
            
        maxIndex = scores.index(max(scores));
        membership = community_to_membership(dendro.merges,g.vcount(),maxIndex);
        return membership;
    
    
    
    def getGroupsFromMembership(self,membership):
        groups  = {};
        for i in range(0,len(membership)):
            mod = str(membership[i]);
            cl = self.gen.reverse_dict()[i];
            
            
            # filter owl:Thing node
            if cl == "http://www.w3.org/2002/07/owl#Thing":
                continue;
            
            # filter non-local nodes
            if not str(cl).startswith(self.ns):
                continue
            
            if mod in groups:
                groups[mod].append(cl);
            else:
                group = [cl];
                groups[mod] = group;
            
        return groups;
    
    
    def extendGroupsWithProperties(self,groups,unusedPropertyGroup):
        # Create a list of properties in the schema.
        graph = self.spec.graph
        proptypes = [RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty]
        proplist = []
        for onetype in proptypes: 
            for sub in graph.subjects(RDF.type, onetype):
                uri = str(sub)
                if uri.startswith(self.ns) and not sub in proplist:
                    proplist.append(sub)
        
        #print("found: "+str(len(proplist)) + " properties");
        
        #now we have our local properties
        for p in proplist:
            puri = str(p);
            #localProp = str(p.uri).replace(ns,"");
            
            added = False;
            for dStmt in graph.objects(p, RDFS.domain):
                domClass = str(dStmt);
                #check if local ns;
                if not domClass.startswith(self.ns):
                    continue;
                            
                #localName = domClass.replace(ns, "");
                
                #find correct group
                for gid in groups.keys():
                    group = groups[gid];
                    if domClass in group:
                        
                        added = True;
                        if not puri in group:
                        
                            #print("Adding "+str(p.uri) +" to group "+str(id));
                            group.append(puri);
                            
            # if not added to domain site, look at range site for possible group
            if not added:
                for rStmt in graph.objects(p, RDFS.range):
                    rangeClass = str(rStmt);
                    #check if local ns;
                    if not rangeClass.startswith(self.ns):
                        continue;
                            
                    #localName = rangeClass.replace(ns, "");
                
                    #find correct group
                    for gid in groups.keys():
                        group = groups[gid];
                        if rangeClass in group:
                        
                            added = True;
                            if not puri in group:
                        
                                #print("Adding "+str(p.uri) +" to group "+str(id));
                                group.append(puri);
                    
            # if not added to a group -- create 'special' unused group
            if (unusedPropertyGroup):
                unusedG = 'otherProperties';
                if not added:
                    if unusedG in groups:
                        group = groups[unusedG];
                        if not puri in group:
                            group.append(puri);
                    else:
                        group = [puri];
                        groups[unusedG] = group;
                    #print("Added to unused : "+localProp);
            
        
        return groups;
    
    

    
    
    def createHTML(self,groups,labels):
        html ='<div id="terms_grouped"> ';
        for gid in groups:
            group = groups[gid];
            if gid in labels:
                label = labels[gid];
            else:
                label = gid;
            html +='<div class="group_table">\n<h3>'+label+'</h3><ul>\n';
            for con in group:
                html += '<li><a href="#'+getLocalNameFromString(con)+'">'+getLocalNameFromString(con)+'</a></li>\n';
            html += '</ul></div>\n';
        html += '</div>\n';
        return html
    
    
    def getHTMLGroups(self):
        print("creating groups")
        g,clObj = self.createConceptGraph();
        membership = self.processWalktrap(g);

        groups = self.getGroupsFromMembership(membership);
        #print(groups);
        groups = self.extendGroupsWithProperties(groups,False);
        #print(groups);
        print('creating labels for groups')
        l = Labeling(self.spec,groups,clObj,self.ns)
        labels = l.createLCALabels();
        print("create html for groups")
        html = self.createHTML(groups,labels);
        print("processing of groups finished")
        return html;
    
    
    
    
class Labeling(object):    
    
    def __init__(self, spec,groups,groupObjects,ns):
        self.spec = spec;
        self.groups = groups;
        self.groupObj = groupObjects;
        self.ns = ns;
    
    
    
    def createLCALabels(self):
        labelMap = {};
        for gID in self.groups:
            group = self.groups[gID];
            label = self.getLCALabelForGroup(group);
            labelMap[gID]= label;
        return labelMap;
    
    
    def getLCALabelForGroup(self,group):
        #print("Get Label for Group:");
        #print(getStringForList(group,self.ns));
        
        if len(group)== 1:
            return group[0].replace(self.ns, "")

        label='';
        lcalist = [];
        for uri in group:
            for cl in self.groupObj:
                if str(cl) == uri:
                    lcalist.append(cl);
                    
        if len(lcalist)== 0:
            print("no lca found for this group return: Properties")
            return "Properties";
        else:
            if len(lcalist)==1:
                #print("lca: "+str(lcalist[0]).replace(self.ns, ""));
                label = str(lcalist[0]).replace(self.ns, "");
                return label;
            
            lcalist = self.getLowestCommonAnchestor(lcalist,[]);
            label = self.getStringLabel(lcalist);
            #print("lca: "+ label);
            return label;
        
    
    
    def getLCA(self,u,v):
        
        def getPaths(r,paths):
             
            found = False;
        
            for upper in self.spec.graph.objects(r,RDFS.subClassOf):
                #add object to path
                paths.append(upper);
                found = True;
                paths = getPaths(upper, paths);
                break;
        
            if not found:
                thingnode = OWL.Thing
                paths.append(thingnode);
        
            return paths;
        
        
        pathU = [u];
        pathV = [v];
        
        #get path to root from u;
        pathU = getPaths(u, pathU);
        #get path to root from v;
        pathV = getPaths(v, pathV);
        
        #find first common resource in both paths
        
        common = [x for x in pathU if x in pathV]
        
        if len(common)== 0:
            return None;
        else:
            return common[0];
    
    def getLowestCommonAnchestor(self,LCAList,compared):
        if len(LCAList)==1:
            return LCAList;
        
        for i in range(0,len(LCAList)-1):
            for j in range(i+1,len(LCAList)):
                u = LCAList[i];
                v = LCAList[j];
                # print("u: "+str(u).replace(self.ns, "")+" v: "+str(v).replace(self.ns, ""));
                if ((u,v) in compared) or ((v,u) in compared):
                    #print("has been compared before - skip")
                    continue
                else:
                    compared.append((u,v))
               
                lca = self.getLCA(u,v);
                
                
                if (lca == None or str(lca) =="http://www.w3.org/2002/07/owl#Thing"):
                    continue;
                else:
                    LCAList.remove(u);
                    LCAList.remove(v);
                    if (lca not in LCAList):
                        LCAList.append(lca);
                    return self.getLowestCommonAnchestor(LCAList,compared);
                    
                    
        return LCAList;
    
    
    
    def getStringLabel(self,lcalist):
        
        if len(lcalist)== 0:
            return "";
        
        if len(lcalist)==1:
            return getLocalNameFromURI(lcalist[0]);
        label ="";
        for i in range(0,len(lcalist)-1):
            label = label + getLocalNameFromURI(lcalist[i])+", ";
        
        #print("LABEL:"+label);
        label = label[0:len(label)-2]+ " and "+getLocalNameFromURI(lcalist[len(lcalist)-1]);
        return label;
    
    
    
    
if __name__ == "__main__":
    xlist = [1,2,3,4,5,6,7,8,9,10]
    for x in xlist:
        print("Groups",x)
        print(verteil(x,4,1.5))
    