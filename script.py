#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zeep
import sys

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from pymongo import MongoClient
import xmltodict


print "Login into the Server Just for show, need to be debugged."
wsdl = 'http://sistemas.cvm.gov.br/webservices/Sistemas/SCW/CDocs/WsDownloadInfs.asmx?WSDL'
client = zeep.Client(wsdl=wsdl)
soap_header = client.service.Login('2293', '8700')
soap_header['header']


header = {
    'sessaoIdHeader': {
        'Guid': '2d572807-3eba-4fde-8a9c-8b1bfd503a43',
        'IdSessao': 822240093L,
        '_attr_1': None
    }
}

doc  = '209'
dataDocs = '2016-12-01'
motivo = 'Download documentos, mes 12'

print "Making request", doc, dataDocs, motivo

result_docs = client.service.solicAutorizDownloadArqComptc(_soapheaders=header, iCdTpDoc=doc, strDtComptcDoc=dataDocs, strMotivoAutorizDownload=motivo)

url_docs = result_docs['body']['solicAutorizDownloadArqComptcResult']

print "Downloading and unziping", url_docs

url = urlopen(url_docs)

zipfile = ZipFile(StringIO(url.read()))
lines = None
for name in zipfile.namelist():
    lines = zipfile.open(name).readlines()

data = xmltodict.parse(''.join(lines))

client = MongoClient('localhost', 27017)
db = client.CVM
informes_collection = db.informes
for informe in data['ROOT']['INFORMES']['INFORME_DIARIO']:
    informes_collection.insert_one(informe)