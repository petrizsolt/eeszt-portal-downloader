# EESZT portal downloader

EESZT portalról tölthetünk le törzseket csv fájlba a segítségével.

paraméterek nélküli indítás esetén a 'prod' EESZT portalról tölti le egy 'output.csv' fájlba a 'PUBLIKUS_ORVOS' törzet ';' delimiterrel és 50-es oldalmérettel.

### Átparaméterezhető a kódba a következő globális változókkal:

- PORTAL_URL = 'https://portal.eeszt.gov.hu/torzspublikacio-portlet/rest/torzsvizualizacio/getEntity'
- ENTITY_NAME = 'PUBLIKUS_ORVOS.PUBLIKUS_ORVOS.M'
- OUT_FILE = 'output.csv'
- CSV_SEPARATOR = ';'
- TOTAL_DOWNLOADED = 0
- TOTAL_IN_PORTAL = 0
- PAGE_SIZE = 50

### Parancssori argumentumokkal:
- -torzs: a letölteni kívánt eeszt törzs azonosítója. (portalon f12 developerbe megnézhetjük a törzsek azonosítóját pl.
https://portal.eeszt.gov.hu/torzspublikacio-portlet/rest/torzsvizualizacio/getEntity?entityId=T_ORSZAG.T_ORSZAG.K&page=0&size=5&_ts_=1686734925770 url hivás esetán a törzs azonosító: 'T_ORSZAG.T_ORSZAG.K')
- -output: a kimeneti fájl neve és kiterjesztése pl. eredmeny.csv
- -url: az eeszt portal urlje (ha például tst2 vagy devről akarunk letölteni)
- -csv_sep: csv fájlba mi legyen az elválasztó karakter(csak 1 karakter adható meg)
- -page_size: mekkora legyen az oldalankénti letöltés mérete
