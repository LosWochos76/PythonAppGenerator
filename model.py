import yaml
from entity import Entity

class Model:
    __document = any
    __entities = []
    
    def get_name(self):
        return self.__document['meta']['name']
    
    name = property(get_name)
    
    def get_ui_name(self):
        return self.__document['meta']['ui_name']
    
    ui_name = property(get_ui_name)
    
    def get_entities(self):
        return self.__entities
    
    entities = property(get_entities)

    def get_entity_by_name(self,name):
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None

    def __init__(self):
        with open('system.yaml', 'r') as file:
            self.__document = yaml.safe_load(file)

        for obj in self.__document['entities']:
            self.__entities.append(Entity(self, obj))