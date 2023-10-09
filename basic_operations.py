# Software Name: basic_operations.py
# SPDX-FileCopyrightText: Copyright (c) 2023 Universidad de Cantabria
# SPDX-License-Identifier: LGPL-3.0 
#
# This software is distributed under the LGPL-3.0 license;
# see the LICENSE file for more details.
#
# Author: Laura MARTIN <lmartin@tlmat.unican.es> et al.

import requests, csv
import numpy as np
import pandas as pd
from geopy import distance
from dateutil import parser

LONGITUDE = [-3.883333, -3.7625]; LATITUDE = [43.425, 43.481944]

def get_timestamp(date):
  try:
    return parser.parse(date).timestamp()
  except:     
    return date.timestamp()

def get_date(date):
  return parser.parse(date)

def get_minutes(date):
  try:
    return parser.parse(date).minute
  except:     
    return date.minute

def get_hour(date):
  try:
    return parser.parse(date).hour
  except:     
    return date.hour

def weighted_mean(a, b, alpha):
  return (alpha*a+(1-alpha)*b)

def arithmetic_mean(a):
  return sum(a) / len(a)

def euclidean_distance(a, b):
  return np.linalg.norm(a-b)

def check_coordinates(longitude, latitude): 
  return (LONGITUDE[0] <= longitude <= LONGITUDE[1] and LATITUDE[0] <= latitude <= LATITUDE[1])

def get_aemet_value(coords):
  santander = (43.4911111,-3.8005556)
  santanderairport = (43.4286111,-3.8313889)
  coordenates = (coords[1], coords[0])

  distance_santander = distance.distance(santander, coordenates).km
  distance_santanderairport = distance.distance(santanderairport, coordenates).km

  total = distance_santander + distance_santanderairport
  weigth_santander = 1 - (distance_santander/total)
  
  iterator = 0
  # Estación AEMETT Santander Ciudad
  url = "http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_1111X_datos-horarios.csv?k=can&l=1111X&datos=det&w=0&f=temperatura&x=h24"
  headers = {}; payload={}
  response = requests.request("GET", url, headers=headers, data=payload)
  if response.status_code != 200:
    santander_error = True
  else:
    santander_error = False
    lines = response.text.splitlines()
    reader = csv.reader(lines)
    for row in reader:
      if iterator == 4:
        value1 = float(row[1])
        break
      iterator = iterator + 1  

  iterator = 0
  # Estación AEMETT Santander Aeropuerto
  url = "http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_1109X_datos-horarios.csv?k=can&l=1109X&datos=det&w=0&f=temperatura&x=h24"
  headers = {}; payload={}
  response = requests.request("GET", url, headers=headers, data=payload)
  if response.status_code != 200:
    santanderairport_error = True
  else:
    santanderairport_error = False
    lines = response.text.splitlines()
    reader = csv.reader(lines)
    for row in reader:
      if iterator == 4:
        value2 = float(row[1])
        break
      iterator = iterator + 1 

  if santander_error:
    if santanderairport_error:
      value = False
    else:
      value = value2
  else:
    value = round(weighted_mean(value1, value2, weigth_santander),2)

  return value

def get_surrounding_values(input, distance_required, data_entities, quality_entities):
  values = []
  inputCoords = (input['location']['value']['coordinates'][1], input['location']['value']['coordinates'][0])

  if len(data_entities) != 0: 
    for (i, j) in zip(data_entities, quality_entities):
      if j['outlier']['value']['isOutlier']['value'] == "False":
        if distance.distance(inputCoords, (i['location']['value']['coordinates'][1],i['location']['value']['coordinates'][0])).m <= distance_required:
          values.append([i["value"]['value']])
  else:
    values = []

  return values