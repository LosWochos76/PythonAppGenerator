from attribute import Attribute
from relation import Relation

class Entity:
    __model = any
    __data = any
    __attributes = []
    __relations = []
    
    def get_name(self):
        return list(self.__data)[0]
    
    name = property(get_name)
    
    def get_attributes(self):
        return self.__attributes

    attributes = property(get_attributes)

    def get_attributes_for_table(self):
        for attr in self.attributes:
            if attr.include_in_table:
                yield attr

    attributes_for_table = property(get_attributes_for_table)

    def get_attribute_by_name(self,name):
        for attr in self.attributes:
            if attr.name == name:
                return attr

        return None

    def get_orderby(self):
        if 'orderby' in self.__data[self.name].keys():
            name = self.__data[self.name]['orderby']
            return self.get_attribute_by_name(name)
        else:
            return None

    orderby = property(get_orderby)

    def get_relations(self):
        return self.__relations

    relations = property(get_relations)

    def get_has_relations(self):
        return len(self.__relations) > 0
    
    has_relations = property(get_has_relations)

    def get_distinct_targets(self):
        result = []
        for rel in self.relations:
            if not rel.target in result:
                result.append(rel.target)
        return result

    distinct_targets = property(get_distinct_targets)

    def __init__(self,model,data):
        self.__model = model
        self.__data = data
        self.__attributes = []
        self.__relations = []

        for obj in self.__data[self.name]['attributes']:
            attribute = Attribute(self.__model, obj)
            self.__attributes.append(attribute)

        if 'relations' in self.__data[self.name].keys():
            for obj in self.__data[self.name]['relations']:
                relation = Relation(self.__model, obj)
                self.__relations.append(relation)
