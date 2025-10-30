import xml.etree.ElementTree as ET

tree = ET.parse("currency.xml")
root = tree.getroot()
numcode_charcode = {}
for valute in root.findall("Valute"):
    num_code = valute.find("NumCode").text
    char_code = valute.find("CharCode").text
    numcode_charcode[num_code] = char_code
print("NumCode -> CharCode字典：\n", numcode_charcode)