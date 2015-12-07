import xml.etree.ElementTree as ET
tree = ET.parse('23330124_real.xml')
root = tree.getroot()
print root.tag
for child in root:
	print child.tag, child.attrib
#root = ET.fromstring(country_data_as_string)