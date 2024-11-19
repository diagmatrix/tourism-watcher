"""
Global constants used in the module
"""

JA_URL = "https://www.juntadeandalucia.es/organismos/turismoyandaluciaexterior/areas/turismo/registro-turismo/buscador-establecimientos-servicios-turisticos.html"
""" JA URL to search for tourism registers """

CSS_ACTIVITY = "//select[@id='tipo_objeto_id']"
""" CSS Xpath for the different tourism registers types selector """

TOURIST_APARTMENTS = "Apartamento turístico"
""" Activity name for tourist apartments registers """

RURAL_HOMES = "Casa rural"
""" Activity name for rural homes registers """

TOURIST_HOMES = "Vivienda de uso turístico"
""" Activity name for tourist homes registers """

RURAL_TOURIST_HOMES = "Vivienda turística de alojamiento rural"
""" Activity name for rural tourist homes registers """

CSS_PROVINCE = "//select[@id='provincia']"
""" CSS Xpath for the province selector """

PROVINCE_NAME = "GRANADA"
""" Province name """

CSS_MUNICIPALITY = "//select[@id='municipio']"
""" CSS Xpath for the municipality selector """

MUNICIPALITY_NAME = "GRANADA"
""" Municipality name """

CSS_SEARCH = "//input[@id='buscar']"
""" CSS Xpath for the search button """

CSS_RESULTS = "controlPaginacion"
""" CSS selector for the results """

CSS_EXCEL = "a[onclick='exportarExcel()']"
""" CSS selector for the excel export button """

EXPORTED_FILENAME = "exportacion.xlsx"
""" Excel exported file name """
