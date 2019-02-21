__description__ = """
The ET.Element gets expanded (monkey patched) with the following methods stored in ElementalExpansion before allocation.
The Element can be monkeypached by importing xmlschema, as opposed to using the __builtin__ workaround. Basically, I am piggybacking my monkeypatch on it, meaning that I don't need to copypaste from SO.

    ET.Element.ns_strip()  #returns the tag with the {namespace}
    ET.Element.is_tag(value) # boolean fx to check if tag == value
    ET.Element.describe # prints the content of the elemtn for debugging, similarly to dump but better.
    ET.Element.is_human() # boolean fx to check if human or dancer
    ET.Element.has_attr(key, opt_value) # boolean fx to check if it has key and optionally it key has the given value

To use: `from ET_monkeypatch import ET`
"""

import xmlschema # needed to piggyback the monkeypatch. No schema validation used.
import xml.etree.ElementTree as ET
import re

#### Expanding element tree element...
class ElementalExpansion:
    """
    This is a collection of methods that helps handle better the ET.Element instnaces. They are monkeypatched to the class object itself.
    """

    def ns_strip(self, ns='{http://uniprot.org/uniprot}'):
        return self.tag.replace(ns, '').replace('ns0', '').replace('{', '').replace('}', '')

    def is_tag(self, tag):
        if self.ns_strip() == tag:
            return True
        else:
            return False

    def describe(self):
        print('*' * 10)
        print('element', self)
        print('tag', self.tag)
        print('text', self.text)
        print('tail', self.tail)
        print('attr', self.attrib)
        print([child for child in self])
        print('*' * 10)

    def is_human(self):
        for elem in self:
            if elem.is_tag('organism'):
                for organism_el in list(elem):
                    if organism_el.text == 'Human':
                        return True
        else:
            return False

    def has_attr(self, key, value=None):
        if key in self.attrib:
            if not value:
                return True
            elif self.attrib[key] == value:
                return True
        return False

    def has_text(self):
        if re.match('\w', self.text):
            return True
        else:
            return False


ET.Element.ns_strip = ElementalExpansion.ns_strip
ET.Element.is_tag = ElementalExpansion.is_tag
ET.Element.describe = ElementalExpansion.describe
ET.Element.is_human = ElementalExpansion.is_human
ET.Element.has_attr = ElementalExpansion.has_attr
ET.Element.has_text = ElementalExpansion.has_text
