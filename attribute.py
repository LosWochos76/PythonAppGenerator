class Attribute:
    __model = any
    __data = any
    
    def get_name(self):
        return list(self.__data)[0]
    
    name = property(get_name)

    def get_csharp_name(self):
        return self.name.capitalize()

    csharp_name = property(get_csharp_name)

    def get_type(self):
        return self.__data[self.name]['type']

    type = property(get_type)

    def get_csharp_type(self):
        if self.type == "int":
            return "int"
        
        return "string"
    
    csharp_type = property(get_csharp_type)

    def get_typescript_type(self):
        if self.type == "int":
            return "number"

        return "string"
    
    typescript_type = property(get_typescript_type)

    def get_typescript_default_value(self):
        if self.type == "int":
            return "0"

        return "''"

    typescript_default_value = property(get_typescript_default_value)

    def get_include_in_table(self):
        return self.__data[self.name]['include_in_table']
    
    include_in_table = property(get_include_in_table)

    def get_ui_name(self):
        return self.__data[self.name]['ui_name']

    ui_name = property(get_ui_name)

    def __init__(self,model,data):
        self.__model = model
        self.__data = data
