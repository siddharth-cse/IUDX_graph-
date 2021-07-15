import rdflib
import json
import os
import glob


#list of IRIs to be added in context 
iudx='https://voc.iudx.org.in/'    #IUDX IRI
schema='http://schema.org/'		   #Schema.org IRI
geojson='https://purl.org/geojson/vocab#'   #geojson IRI 
Fiware='https://uri.fiware.org/ns/data-models#'   #Fiware IRI
GTFS='http://vocab.gtfs.org/gtfs.ttl#'		#GTFS IRI
open311 = "http://ontology.eil.utoronto.ca/open311.owl#"  #open311 IRI



#Default dict elements
Model_dict={'@graph':[],
			'@context:':{
			"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
			"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
			"owl": "http://www.w3.org/2002/07/owl#",
			"iudx": "https://voc.iudx.org.in/",
			"skos": "http://www.w3.org/2004/02/skos/core#",
			"schema": "http://schema.org/",
			"geojson": "https://purl.org/geojson/vocab#",
			"Fiware": "https://uri.fiware.org/ns/data-models#",
			"GTFS" : "http://vocab.gtfs.org/gtfs.ttl#",
			"open311" :"http://ontology.eil.utoronto.ca/open311.owl#"}
	        }

#Below lists and loops iterate over all classes



Class_folders=[]        #list storing all JSONLDs for classes

Class_folders.extend(glob.glob('iudx-voc-master/data-models/*/classes/*'))
Class_folders.extend(glob.glob('iudx-voc-master/base-schemas/classes/*'))
Class_folders.extend(glob.glob('iudx-voc-master/data-types/classes/*'))
Class_folders.extend(glob.glob('iudx-voc-master/data-models/classes/*'))


for iudx_class in Class_folders:
	myfile = open(iudx_class.replace('\\','/'))
	class_data = json.load(myfile)
	#print((data['@graph'][0]['rdfs:comment']))
	class_dict={
		"@id": iudx+(class_data['@graph'][0]['@id'].split(':')[1]),
		"@type": 'owl:Class',
		'comment' : (class_data['@graph'][0]['rdfs:comment']),
		'label' : (class_data['@graph'][0]['rdfs:label']),
		'isDefinedBy' : iudx
		}
	#To define subclass item inside @graph
	if('rdfs:subClassOf' in class_data['@graph'][0]):
		class_dict['subClassOf'] = {"@id":iudx+class_data['@graph'][0]['rdfs:subClassOf']['@id'].split(':')[1]}  
	

	#To define exactMatch item inside @graph
	if('skos:exactMatch' in class_data['@graph'][0]):
		
		#Linking schema.org IRI to the matched @id
		if('schema' in class_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			class_dict['skos:exactMatch'] = {"@id": schema + class_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[1]}

		#Linking geojson IRI to the matched @id
		if('geojson' in class_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			class_dict['skos:exactMatch'] = {"@id": geojson + class_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[1]}


	if('skos:closeMatch' in class_data['@graph'][0]):
		if('schema' in class_data['@graph'][0]['skos:closeMatch']['@id'].split(':')[0]):
			class_dict['skos:closeMatch'] = {"@id": schema + class_data['@graph'][0]['skos:closeMatch']['@id'].split(':')[1]}
	

	Model_dict['@graph'].append(class_dict)



#Below lists and loops iterate over all classes

Properties_folders=[]     #list storing all JSONLDs for properties

Properties_folders.extend(glob.glob('iudx-voc-master/data-models/*/properties/*'))
Properties_folders.extend(glob.glob('iudx-voc-master/base-schemas/properties/*'))


for iudx_properties in Properties_folders:
	myfile = open(iudx_properties.replace('\\','/'))
	properties_data = json.load(myfile)
	properties_dict={
		"@id": iudx+(properties_data['@graph'][0]['@id'].split(':')[1]),
		"@type": properties_data['@graph'][0]['@type'],
		'comment' : (properties_data['@graph'][0]['rdfs:comment']),
		'label' : (properties_data['@graph'][0]['rdfs:label']),
		'isDefinedBy' : iudx,
		'iudx:domainIncludes' : properties_data['@graph'][0]['iudx:domainIncludes'],
		'iudx:rangeIncludes' : properties_data['@graph'][0]['iudx:rangeIncludes']
		}

	#To define exactMatch item inside @graph
	if('skos:exactMatch' in properties_data['@graph'][0]):
		#print(properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0],iudx_properties)


		#Linking Fiware IRI to the matched @id
		if(('fiware') in properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0] or('Fiware') in properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			properties_dict['skos:exactMatch'] = {"@id": Fiware + properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[1].strip()}
			#print(properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0],iudx_properties)

		#Linking schema IRI to the matched @id
		if(('schema') in properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			properties_dict['skos:exactMatch'] = {"@id": schema + properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[1].strip()}
			#print(properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0],iudx_properties)


		#Linking GTFS IRI to the matched @id
		if(('GTFS') in properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			properties_dict['skos:exactMatch'] = {"@id": GTFS + properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[-1].strip()}
			#print(properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0],iudx_properties)


		#Linking open311 IRI to the matched @id
		if(('open311') in properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			#print(properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0],iudx_properties)			
			properties_dict['skos:exactMatch'] = {"@id": open311 + properties_data['@graph'][0]['skos:exactMatch']['@id'].split(':')[-1].strip()}
		







	#if('iudx:domainIncludes' in properties_data['@graph'][0]):
	#	print(properties_data['@graph'][0]['iudx:domainIncludes'])



	Model_dict['@graph'].append(properties_dict)









with open("Model.jsonld", "w") as outfile:
	json.dump(Model_dict, outfile,indent=4, sort_keys=True)
