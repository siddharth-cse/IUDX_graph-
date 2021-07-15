import rdflib
import json
import os
import glob

iudx='https://voc.iudx.org.in/'    #IUDX IRI
schema='http://schema.org/'
geojson='https://purl.org/geojson/vocab#'


#Default dict elements
Model_dict={'@graph':[],
			'@context:':{
			"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
	        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
	        "owl": "http://www.w3.org/2002/07/owl#",
	        "iudx": "https://voc.iudx.org.in/",
	        "skos": "http://www.w3.org/2004/02/skos/core#",
        	"schema": "http://schema.org/",
        	"geojson": "https://purl.org/geojson/vocab#"}
	        }


Class_folders=[]

Class_folders.extend(glob.glob('iudx-voc-master/data-models/*/classes/*'))
Class_folders.extend(glob.glob('iudx-voc-master/base-schemas/classes/*'))
Class_folders.extend(glob.glob('iudx-voc-master/data-types/classes/*'))
Class_folders.extend(glob.glob('iudx-voc-master/data-models/classes/*'))


for iudx_class in Class_folders:
	myfile = open(iudx_class.replace('\\','/'))
	data = json.load(myfile)
	#print((data['@graph'][0]['rdfs:comment']))
	class_dict={
		"@id": iudx+(data['@graph'][0]['@id'].split(':')[1]),
		"@type": 'owl:Class',
		'comment' : (data['@graph'][0]['rdfs:comment']),
		'label' : (data['@graph'][0]['rdfs:label']),
		'isDefinedBy' : iudx
		}
	#To define subclass item inside @graph
	if('rdfs:subClassOf' in data['@graph'][0]):
		class_dict['subClassOf'] = {"@id":iudx+data['@graph'][0]['rdfs:subClassOf']['@id'].split(':')[1]}  
	

	#To define exactMatch item inside @graph
	if('skos:exactMatch' in data['@graph'][0]):

		print(data['@graph'][0]['skos:exactMatch'])
		
		#Linking schema.org IRI to the matched @id
		if('schema' in data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			class_dict['skos:exactMatch'] = {"@id": schema + data['@graph'][0]['skos:exactMatch']['@id'].split(':')[1]}

		#Linking geojson IRI to the matched @id
		if('geojson' in data['@graph'][0]['skos:exactMatch']['@id'].split(':')[0]):
			class_dict['skos:exactMatch'] = {"@id": geojson + data['@graph'][0]['skos:exactMatch']['@id'].split(':')[1]}


	if('skos:closeMatch' in data['@graph'][0]):
		print(data['@graph'][0]['skos:closeMatch'])


	Model_dict['@graph'].append(class_dict)




with open("Model.jsonld", "w") as outfile:
    json.dump(Model_dict, outfile,indent=4, sort_keys=True)
