class Relation:
    __model = any
    __data = any
    
    def get_name(self):
        return list(self.__data)[0]
    
    name = property(get_name)

    def get_csharp_name(self):
        return self.name.capitalize()

    csharp_name = property(get_csharp_name)

    def get_ui_name(self):
        return self.__data[self.name]['ui_name']

    ui_name = property(get_ui_name)

    def get_target(self):
        target = self.__data[self.name]['target']
        return self.__model.get_entity_by_name(target)
    
    target = property(get_target)

    def get_cardinality(self):
        return self.__data[self.name]['cardinality']

    cardinality = property(get_cardinality)

    def __init__(self,model,data):
        self.__model = model
        self.__data = data
    
