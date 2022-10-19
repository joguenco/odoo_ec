# -*- coding: utf-8 -*-
import paxb as px
from xml.dom.minidom import parseString


@px.model
class Invoice:
    id = px.attribute()
    version = px.attribute()
    customer = px.field(name="cliente")
    date = px.field(name="fecha")


obj = Invoice(id='comprobante',
              version='1.1.0',
              customer='Jorge Luis',
              date='2022-10-19')

xml = px.to_xml(obj, name='factura', encoding='unicode')

print(xml)

xml_pretty = parseString(xml).toprettyxml(
        indent=' ' * 2, 
        encoding="utf-8"
        ).decode("utf-8")

print(xml_pretty)

file = open("01102022.xml", "w")
file.write(xml_pretty)
file.close()

