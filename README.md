# EESZT portal downloader

EESZT portalról tölthetünk le törzseket csv fájlba a segítségével.

paraméterek nélküli indítás esetén a 'prod' EESZT portalról tölti le egy 'output.csv' fájlba a 'PUBLIKUS_ORVOS' törzet ';' delimiterrel és 50-es oldalmérettel.

# H3: Átparaméterezhető a kódba a következő globális változókkal:

- PORTAL_URL = 'https://portal.eeszt.gov.hu/torzspublikacio-portlet/rest/torzsvizualizacio/getEntity'
- ENTITY_NAME = 'PUBLIKUS_ORVOS.PUBLIKUS_ORVOS.M'
- OUT_FILE = 'output.csv'
- CSV_SEPARATOR = ';'
- TOTAL_DOWNLOADED = 0
- TOTAL_IN_PORTAL = 0
- PAGE_SIZE = 50
