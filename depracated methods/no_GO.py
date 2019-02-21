## GO has been removed.


## settings_handler Settings used to have
class GlobalSettings:
    @property
    def go(self):
        current = None
        if self._obodict:
            pass
        else:
            for row in self.open('go'):
                if '[Term]' in row or not row:
                    current = None
                elif GO.is_key(row, 'id'):
                    current = GO.get_GO(row)
                    self._obodict[current] = GO(current)
                elif current:
                    key = GO.get_key(row)
                    if not key:
                        continue
                    elif key in ('name', 'namespace', 'def', 'subset', 'xref'):
                        setattr(self._obodict[current], key, GO.get_value(row))
                    elif key in ('synomym'):
                        getattr(self._obodict[current], key).append(GO.get_value(row))
                    elif key in ('is_a', 'disjoint_from', 'intersection_of'):
                        getattr(self._obodict[current], key).append(GO.get_GO(row))
                else:
                    pass
        return self._obodict


# while protein paesing from uniprot had self.GO = [(xref['id'], xref['property'][0]['value']) for xref in clean_dict['dbReference'] if xref['type'] == 'GO']
