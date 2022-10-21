# -*- coding: utf-8 -*-
import paxb as px
from xml.dom.minidom import parseString
from lxml import etree
from io import BytesIO


@px.model
class Invoice:
    id = px.attribute()
    version = px.attribute()
    customer = px.field(name="cliente")
    date = px.field(name="fecha")
    guide = px.field(name="guia")


obj = Invoice(id='comprobante',
              version='1.1.0',
              customer='Jorge Luis',
              date='2022-10-19',
              guide='')

xml = px.to_xml(obj, name='factura', encoding='unicode')

print(xml)

file = open("01102022.xml", "w")
file.write(xml)
file.close()

tree = etree.parse("01102022.xml")

for elem in tree.xpath('//*[not(node())][not(count(./@*))>0]'):
   elem.getparent().remove(elem)

with open("01102022.xml","wb") as f:
    f.write(
            etree.tostring(tree, 
                xml_declaration=True, 
                encoding='utf-8')
            )

xml_pretty = None
with open("01102022.xml", "r+") as xmlFile:
    # Reading form a file
    xml = xmlFile.read()

    xml_pretty = parseString(xml).toprettyxml(
            indent=' ' * 2, 
            encoding="utf-8"
            ).decode("utf-8")

    print(xml_pretty)

    xmlFile.close()

file = open("01102022.xml", "w")
file.write(xml_pretty)
file.close()
