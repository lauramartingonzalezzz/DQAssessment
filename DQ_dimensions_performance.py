# Software Name: DQ_dimensions_performance.py
# SPDX-FileCopyrightText: Copyright (c) 2023 Universidad de Cantabria
# SPDX-License-Identifier: LGPL-3.0 
#
# This software is distributed under the LGPL-3.0 license;
# see the LICENSE file for more details.
#
# Author: Laura MARTIN <lmartin@tlmat.unican.es> et al.

# Propietary files
import basic_operations
import context_broker_api
import configuration_variables

# Imports
import math, time, random
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

import sys, os
sys.path.append('../')


# Accuracy
def accuracy_request(input):
  ground_truth = basic_operations.get_aemet_value(input['location']['value']['coordinates'])
  return ground_truth

def accuracy_processing(input, ground_truth):
  accuracy = (
    round(abs(input['value']['value'] - ground_truth),2)
    if ground_truth
    else 0
  )
  return accuracy


# Completeness
def completeness_request(input):  
  quality_temporal, error = context_broker_api.get_temporal_values_by_id(input['hasQuality']['object'], "DataQualityAssessment", input['dateModified']['value'])
  if error: return None, True

  return quality_temporal, False

def completeness_processing(is_synthetic, quality_temporal):
  n = int(is_synthetic)
  total = 1
	
  if 'synthetic' not in quality_temporal:
    print(quality_temporal)

  if isinstance(quality_temporal['synthetic'], list): # more than one temporal value
    total = total + len(quality_temporal['synthetic'])
    for i in quality_temporal['synthetic']:
      if i['value']['isSynthetic']['value'] == "True":
        n = n + 1
  else: # just one temporal value
    if quality_temporal['synthetic']['value']['isSynthetic']['value'] == "True":
      total = total + 1
      n = n + 1

  completeness = round((total-n)/total,3)*100 # instead of calculating it in terms of time (time_window), I calculate it in terms of observations logged in that time (thanks to the completeness_request, which makes use of the time_window).

  return completeness


# Precision
def precision_request():
  data_entities, error = context_broker_api.get_entities_by_type("Temperature")
  if error: return None, None, True

  quality_entities, error = context_broker_api.get_entities_by_type("DataQualityAssessment")
  if error: return None, None, True

  return data_entities, quality_entities, False

def precision_processing(input, data_entities, quality_entities):
  if len(data_entities) == 0:
    precision = 0 # +-0 degreeCelsius -- 100%
  else:
    input_value = np.array(input["value"]['value'])
    surrounding_values = np.array(basic_operations.get_surrounding_values(input, configuration_variables.distance_range, data_entities, quality_entities))
    
    precision = (
      basic_operations.euclidean_distance(input_value, surrounding_values)/math.sqrt(len(surrounding_values))
      if len(surrounding_values) != 0
      else 0
    )

  return precision


# Timeliness
def timeliness_request(input):
	data_entity, error = context_broker_api.get_entity_by_id(input['id'], input['type'])
	if error: return None, None, True
	if len(data_entity) != 0: data_entity = data_entity[0]

	quality_entity, error = context_broker_api.get_entity_by_id(input['hasQuality']['object'], "DataQualityAssessment")
	if error: return None, None, True
	if len(quality_entity) != 0: quality_entity = quality_entity[0]
	
	return data_entity, quality_entity, False


def timeliness_processing(input, data_entity, quality_entity):
	input_timestamp = basic_operations.get_timestamp(input['dateModified']['value'])
	data_timestamp = basic_operations.get_timestamp(data_entity['dateModified']['value'])

	input_timeliness = round((input_timestamp - data_timestamp)/60, 2)
	data_timeliness = quality_entity['timeliness']['value']

	timeliness = (
		basic_operations.weighted_mean(data_timeliness,input_timeliness,0.8)
		if input_timeliness > 0.5
		else data_timeliness
	)

	return timeliness


# Main
montecarlo_simulations = 60
for i in range(montecarlo_simulations):
	# Directory
	folder_name = "simulations/sim"+str(i)
	path = os.path.join(".", folder_name)
	os.mkdir(path)

	# PRODUCTION
	nsim = 10000 # max_id = 100 x 100 temporal values
	max_id = 100 # 100 different entities
	window = 120 # minutes
	seconds_gen = 1.2 # seconds

	# Filenames
	accuracy_file = folder_name+"/accuracy.csv"
	completeness_file = folder_name+"/completeness.csv"
	precision_file = folder_name+"/precision.csv"
	timeliness_file = folder_name+"/timeliness.csv"

	# Store arrays
	accuracy_request_time = []; accuracy_processing_time = []
	completeness_request_time = []; completeness_processing_time = []
	precision_request_time = []; precison_processing_time = []
	timeliness_request_time = []; timeliness_processing_time = []

	date_object = datetime.now()

	# Randomly created. This script is intended to assess the performance of the DQ dimensions calculation.
	is_synthetic = random.choices(population = [True, False], weights=[0.1, 0.9], k=nsim)
	is_outlier = random.choices(population = [True, False], weights=[0.1, 0.9], k=nsim)

	for j in range(nsim):
		
		# Simulate input
		temperature_value = round(random.uniform(8,25),2)
		longitude_value = round(random.uniform(-3.883333, -3.7625),4)
		latitude_value = round(random.uniform(43.425, 43.481944),4)
		date_value = date_object.strftime('%Y-%m-%dT%H:%M:%SZ')

		if j%max_id == 0: id = 0 # Generation every seconds_gen (1.2 seconds) of different ids --> Generation every 2 min of temporal value

		input = {
			"id": "urn:x-iot:u7jcfa:"+str(id),
			"type": "Temperature",
			"address": {
				"type": "Property",
				"value": {
					"addressCountry": "Spain",
					"addressLocality": "Santander",
					"addressRegion": "Cantabria"
				}
			},
			"areaServed": {
				"type": "Property",
				"value": "Santander"
			},
			"unit": {
				"type": "Property",
				"value": "degreeCelsius"
			},
			"dataProvider": {
				"type": "Property",
				"value": "SmartSantander"
			},
			"dateModified": {
				"type": "Property",
				"value": date_value,
				"observedAt": date_value
			},
			"source": {
				"type": "Property",
				"value": "https://api.smartsantander.eu/"
			},
			"value":{
				"type": "Property",
				"value": temperature_value,
				"observedAt": date_value,
				"unitCode": "CEL"
			},
			"location": {
				"type": "GeoProperty",
				"value": {
						"type": "Point",
						"coordinates": [
							latitude_value,
							longitude_value          
						]
				}
			},
			"@context":["https://raw.githubusercontent.com/SALTED-Project/contexts/main/wrapped_contexts/energycim-context.jsonld"]
		}

		quality_id = "urn:ngsi-ld:DataQualityAssessment:"+str(id)

		# Add the relationship with the dataQualityAssessment entity
		input['hasQuality'] = {"type": "Relationship", "object": quality_id}

		
		# -------------- ACCURACY --------------
		# Request
		start_time = time.time()
		ground_truth = accuracy_request(input)
		final_time = time.time()
		accuracy_request_time.append(final_time - start_time) # IN SECONDS

		# Processing
		start_time = time.time()
		accuracy = accuracy_processing(input, ground_truth)
		final_time = time.time()
		accuracy_processing_time.append(final_time - start_time) # IN SECONDS


		# -------------- COMPLETENESS --------------
		timeAt = date_object - relativedelta(minutes=window) # 120 minutes === 60 entities (generation every 2 minutes)
		timeAt = timeAt.strftime('%Y-%m-%dT%H:%M:%SZ')
		# Request
		start_time = time.time()
		quality_temporal, error = completeness_request(input)
		final_time = time.time()
		completeness_request_time.append(final_time - start_time) # IN SECONDS

		# Processing
		start_time = time.time()
		if error: completeness = 1
		else: 
			if j >= max_id: completeness = completeness_processing(is_synthetic[i], quality_temporal) # First entity
			else: completeness = 1 # First time
		final_time = time.time()
		completeness_processing_time.append(final_time - start_time) # IN SECONDS


		# -------------- PRECISION --------------
		# Request
		start_time = time.time()
		data_entities, quality_entities, error = precision_request()
		final_time = time.time()
		precision_request_time.append(final_time - start_time) # IN SECONDS

		# Processing
		start_time = time.time()
		if error: precision = 0
		else: 
			if j >= max_id: precision = precision_processing(input, data_entities, quality_entities)
			else: precision = 0 # First time
		final_time = time.time()
		precison_processing_time.append(final_time - start_time) # IN SECONDS


		# -------------- TIMELINESS --------------
		# Request
		start_time = time.time()
		data_entities, quality_entities, error = timeliness_request(input)
		final_time = time.time()
		timeliness_request_time.append(final_time - start_time) # IN SECONDS

		# Processing
		start_time = time.time()
		if error: timeliness = 10
		else: 
			if j >= max_id: timeliness = timeliness_processing(input, data_entities, quality_entities)
			else: timeliness = 10
		final_time = time.time()
		timeliness_processing_time.append(final_time - start_time) # IN SECONDS


		# -------------- TAGGING --------------
		quality_input = {
			"id": "urn:ngsi-ld:DataQualityAssessment:"+str(id),
			"type": "DataQualityAssessment",
			"dateCalculated": {
				"type": "Property",
				"value": date_value
			},
			"source": {
				"type": "Property",
				"value": "https://salted-project.eu"
			},
			"outlier": {
				"type": "Property",
				"value": {
				"isOutlier": {
					"type": "Property",
					"value": str(is_outlier[i])
				},
				# "methodology": {
				# 		"type": "Relationship",
				# 		"object": "urn:ngsi-ld:AI-Methodology:Outlier:Temperature:smartsantander:u7jcfa:t508"
				# }
				},
				"observedAt": date_value
			},
			"synthetic": {
				"type": "Property",
				"value": {
				"isSynthetic": {
					"type": "Property",
					"value": str(is_synthetic[i])
				},
				# "methodology": {
				# 		"type": "Relationship",
				# 		"object": "urn:ngsi-ld:AI-Methodology:Synthetic:Temperature:smartsantander:u7jcfa:t508"
				# }
				},
				"observedAt": date_value
			},
			"accuracy": {
				"type": "Property",
				"value": accuracy,
				"observedAt": date_value,
				"unitCode": "CEL"
			},
			"timeliness": {
				"type": "Property",
				"value": timeliness,
				"observedAt": date_value,
				"unitCode": "minutes"
			},
			"precision": {
				"type": "Property",
				"value": precision,
				"observedAt": date_value,
				"unitCode": "CEL"
			},
			"completeness": {
				"type": "Property",
				"value": completeness,
				"observedAt": date_value,
				"unitCode": "P1"
			},
			"@context": ["https://raw.githubusercontent.com/SALTED-Project/contexts/main/wrapped_contexts/dataquality-context.jsonld"]
		}

		# -------------- UPSERT TO CONTEXT BROKER --------------
		status = context_broker_api.upsert_entity(input)
		if status == 204 or status == 201: status = context_broker_api.upsert_entity(quality_input)

		date_object = date_object + relativedelta(seconds = seconds_gen)
		id += 1

	# Store time values
	df = pd.DataFrame()
	df["request_time"] = accuracy_request_time; df["processing_time"] = accuracy_processing_time
	df.to_csv(accuracy_file)  

	df = pd.DataFrame()
	df["request_time"] = completeness_request_time; df["processing_time"] = completeness_processing_time
	df.to_csv(completeness_file)  

	df = pd.DataFrame()
	df["request_time"] = precision_request_time; df["processing_time"] = precison_processing_time
	df.to_csv(precision_file)  

	df = pd.DataFrame()
	df["request_time"] = timeliness_request_time; df["processing_time"] = timeliness_processing_time
	df.to_csv(timeliness_file)  

	context_broker_api.delete_entities()
