import pandas as pd
import numpy as np
import sys
import csv

filename = sys.argv[1]

df = pd.read_csv(filename)

df['ZONE_ID'] = -1


sinzones = {"CENTRO ORIENTE": 1, "VDM SUR": 2, "VDM NORTE": 3, "CENTRO SUR": 4, "VDM CENTRO": 5, "LAZARO CARDENAS": 6, "SAN CRISTOBAL": 7, "VERACRUZ": 8, "IZUCAR": 9, "XALAPA": 10, "COATZACOALCOS": 11, "TECAMACHALCO": 12, "LOS TUXTLAS": 13, "PUEBLA": 14, "POZA RICA": 15, "CHILPANCINGO": 16, "SAN MARTIN": 17, "TLAXCALA": 18, "TUXTLA": 19, "CUAUTLA": 20, "ACAPULCO": 21, "TAPACHULA": 22, "TEHUANTEPEC": 23, "TEZIUTLAN": 24, "IGUALA": 25, "CHONTALPA": 26, "VILLAHERMOSA": 27, "MORELOS": 28, "CORDOBA": 29, "LOS RIOS": 30, "ORIZABA": 31, "HUATULCO": 32, "TEHUACAN": 33, "CENTRO SUR": 34, "CUERNAVACA": 35, "HUAJUAPAN": 36, "ZIHUATANEJO": 37, "OAXACA": 38, "ZAMORA": 39, "SAN LUIS POTOSI": 40, "IRAPUATO": 41, "MORELIA": 42, "CIENEGA": 43, "TEPIC VALLARTA": 44, "SAN JUAN DEL RIO": 45, "GUADALAJARA": 46, "APATZINGAN": 47, "ZACATECAS": 48, "AGUASCALIENTES": 49, "COLIMA": 50, "QUERETARO": 51, "CELAYA": 52, "MINAS": 53, "MANZANILLO": 54, "ZACAPU": 55, "ZAPOTLAN": 56, "IXMIQUILPAN": 57, "LEON": 58, "FRESNILLO": 59, "LOS ALTOS": 60, "MATEHUALA": 61, "URUAPAN": 62, "SALVATIERRA": 63, "JIQUILPAN": 64, "NAVOJOA": 65, "HERMOSILLO": 66, "NOGALES": 67, "CABORCA": 68, "LOS MOCHIS": 69, "CULIACAN": 70, "OBREGON": 71, "GUASAVE": 72, "GUAYMAS": 73, "MAZATLAN": 74, "LAGUNA": 75, "CAMARGO": 76, "JUAREZ": 77, "CUAUHTEMOC": 78, "CHIHUAHUA": 79, "DURANGO": 80, "CASAS GRANDES": 81, "TAMPICO": 82, "HUASTECA": 83, "PIEDRAS NEGRAS": 84, "MONTERREY": 85, "NUEVO LAREDO": 86, "MONCLOVA": 87, "REYNOSA": 88, "SALTILLO": 89, "MONTEMORELOS": 90, "HUEJUTLA": 91, "VICTORIA": 92, "MATAMOROS": 93, "SABINAS": 94, "RIVIERA MAYA": 102, "CAMPECHE": 103, "MERIDA": 104, "CANCUN": 105, "MOTUL TIZIMIN": 106, "CARMEN": 107, "CHETUMAL": 108, "TICUL": 109 }


bcazones = {
	"ENSENADA": 95,
	"MEXICALI": 96,
	"TIJUANA": 98,
	"SANLUIS": 100
}

bcszones = {
	"LOS CABOS": 97,
	"LA PAZ": 99,
	"CONSTITUCION": 101
}


def getMap(sistema):
	return {
		'BCS': bcszones,
		'BCA': bcazones,
		'SIN': sinzones
	}.get(sistema, sinzones)

def getZoneId(row):
	zdc = row['ZONA.DE.CARGA']
	sistema = row['SISTEMA']
	sismap = getMap(sistema)
	return sismap.get(zdc, 110) # NA = 110 default *not found

df['ZONE_ID'] = df.apply(getZoneId, axis = 1)

df[['CLAVE', 'NOMBRE', 'ZONE_ID']].to_csv('nodes_with_id.csv', header=['nodo_id', 'nombre', 'zone_id'], index = False, quoting=csv.QUOTE_NONNUMERIC)

