# Software Name: context_broker_api.pu
# SPDX-FileCopyrightText: Copyright (c) 2023 Universidad de Cantabria
# SPDX-License-Identifier: LGPL-3.0 
#
# This software is distributed under the LGPL-3.0 license;
# see the LICENSE file for more details.
#
# Author: Laura MARTIN <lmartin@tlmat.unican.es> et al.

import requests, json
from dateutil import parser
from dateutil.relativedelta import relativedelta
import configuration_variables

types = configuration_variables.types.split(",")

# upsert_entity: upsert entity into the Context Broker
#     Params: 
#        - body: complete entity body
#     Return: 
#        - status code -- 201 Created / 204 No Content
def upsert_entity(body):
	url = configuration_variables.broker_url + "entityOperations/upsert?options=update"
	payload = json.dumps([body])
	headers = {'Content-Type': 'application/ld+json'}

	response = requests.request("POST", url, headers=headers, data=payload)
	return response.status_code


# check_if_entity_already_exists: check if the entity requested already exists in the Context broker
#     Params: 
#        - entity_id: id of the entity requested
#        - entity_type: type of the entity requested
#     Return: 
#        - True/False: Entity found/not found
#        - error: boolean specifying if there have been any errors throughout the function (associated with requests to the Context Broker or external instances)
def check_if_entity_already_exists(entity_id, entity_type):
  url = configuration_variables.broker_url + "entities/" + entity_id

  context_link = (
    configuration_variables.base_context+entity_type.lower()+'-context.jsonld'
    if entity_type in types
    else configuration_variables.base_context + "default-context.jsonld"
  )

  headers = {
    'Accept': 'application/ld+json',
    'Link': '<'+context_link+'>;rel="http://www.w3.org/ns/json-ld#context"'
  }

  response = requests.request("GET", url, headers=headers, data={})
  if response.status_code == 200: return True, False
  elif response.status_code == 404: return False, False
  else: return None, True
  

# get_entities_by_type_geoQuery: get entities stored in the Context Broker filtering by type and applying a geoQuery
#     Params: 
#        - entity_type: type requested
#        - coordinates: coordinates to make the geoQuery filter
#     Return: 
#        - array of entities
#        - error: boolean specifying if there have been any errors throughout the function (associated with requests to the Context Broker or external instances)
def get_entities_by_type_geoQuery(entity_type, coordinates):
  url = configuration_variables.broker_url + "entities/?type="+entity_type+"&georel=near%3BmaxDistance=="+configuration_variables.distance_range+"&coordinates="+coordinates+"&geometry=Point"

  context_link = (
    configuration_variables.base_context+entity_type.lower()+'-context.jsonld'
    if entity_type in types
    else configuration_variables.base_context + "default-context.jsonld"
  )

  headers = {
    'Accept': 'application/ld+json',
    'Link': '<'+context_link+'>;rel="http://www.w3.org/ns/json-ld#context"'
  }

  response = requests.request("GET", url, headers=headers, data={})

  if response.status_code == 200: return response.json(), False
  else: return None, True


# get_entity_by_id: get last value recorded in the Context Broker of an entity (by its unique id) or several entities (by a string with a list of ids)
#     Params: 
#        - entity_id: id or list of id concatenated as a string with commas e.g.: id1,id2,id3
#        - entity_type: type of the entities requested
#     Return: 
#        - array of entities
#        - error: boolean specifying if there have been any errors throughout the function (associated with requests to the Context Broker or external instances)
def get_entity_by_id(entity_id, entity_type):
  url = configuration_variables.broker_url + "entities/?id=" + entity_id

  context_link = (
    configuration_variables.base_context+entity_type.lower()+'-context.jsonld'
    if entity_type in types
    else configuration_variables.base_context + "default-context.jsonld"
  )

  headers = {
    'Accept': 'application/ld+json',
    'Link': '<'+context_link+'>;rel="http://www.w3.org/ns/json-ld#context"'
  }

  response = requests.request("GET", url, headers=headers, data={})
  if response.status_code == 200: return response.json(), False
  else: return None, True


# get_temporal_values_by_id: get temporal instances of attributes of a determined entity filtered by id and within a time window
#     Params: 
#        - entity_id: id of the requested entity
#        - entity_type: type of the requested entity
#        - entity_date_string: date of the requested entity
#     Return: 
#        - entity with arrays in attributes if there is more thant one temporal instance
#        - error: boolean specifying if there have been any errors throughout the function (associated with requests to the Context Broker or external instances)
def get_temporal_values_by_id(entity_id, entity_type, entity_date_string):
  entity_date = parser.parse(entity_date_string)
  timeAt = (entity_date - relativedelta(minutes=configuration_variables.time_window)).strftime('%Y-%m-%dT%H:%M:%SZ')

  url = configuration_variables.broker_url + "temporal/entities/"+entity_id+"?timerel=after&timeAt="+timeAt+"&lastN="+str(configuration_variables.lastN)

  context_link = (
    configuration_variables.base_context+entity_type.lower()+'-context.jsonld'
    if entity_type in types
    else configuration_variables.base_context + "default-context.jsonld"
  )

  headers = {
    'Accept': 'application/ld+json',
    'Link': '<'+context_link+'>;rel="http://www.w3.org/ns/json-ld#context"'
  }
  
  response = requests.request("GET", url, headers=headers, data={})
  if response.status_code == 200: return response.json(), False
  else: return None, True


def get_entities_by_type(entity_type):
  url = configuration_variables.broker_url + "entities/?type="+entity_type+"&lastN=200"
  
  context_link = (
    configuration_variables.base_context+entity_type.lower()+'-context.jsonld'
    if entity_type in types
    else configuration_variables.base_context + "default-context.jsonld"
  )

  headers = {
    'Accept': 'application/ld+json',
    'Link': '<'+context_link+'>;rel="http://www.w3.org/ns/json-ld#context"'
  }

  response = requests.request("GET", url, headers=headers, data={})

  if response.status_code == 200: return response.json(), False
  else: return None, True


def delete_entities():
  id_list=[]

  # Temperature
  url = configuration_variables.broker_url + "entities/?type=Temperature&limit=1000"
  headers = {
    'Accept': 'application/ld+json',
    'Link': '<https://raw.githubusercontent.com/SALTED-Project/contexts/main/wrapped_contexts/energycim-context.jsonld>;rel="http://www.w3.org/ns/json-ld#context";type="application/ld+json"'
  }
  response = requests.request("GET", url, headers=headers, data={})

  for i in response.json():
    id_list.append(i['id'])

  # DataQualityAssessment
  url = configuration_variables.broker_url + "entities/?type=DataQualityAssessment&limit=1000"
  headers = {
    'Accept': 'application/ld+json',
    'Link': '<https://raw.githubusercontent.com/SALTED-Project/contexts/main/wrapped_contexts/dataquality-context.jsonld>;rel="http://www.w3.org/ns/json-ld#context";type="application/ld+json"'
  }
  response = requests.request("GET", url, headers=headers, data={})

  for i in response.json():
    id_list.append(i['id'])


  # DELETE 
  url = configuration_variables.broker_url + "entityOperations/delete"
  payload = json.dumps(id_list)
  headers = {
    'Content-Type': 'application/ld+json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  if response.status_code != 204: print("DELETE /entities ", response.status_code)


  # DELETE /temporal
  for i in id_list:
      url = configuration_variables.broker_url + "temporal/entities/"+i
      response = requests.request("DELETE", url, headers=headers, data=payload)
      if response.status_code != 204: print("DELETE /temporal/entities ", response.status_code)

