from base_generator import BaseGenerator
from pathlib import Path
import os
from base_generator import BaseGenerator

class CsharpModelGenerator(BaseGenerator):
    def get_project_name(self):
        return self._model.name + ".Model"
    
    project_name = property(get_project_name)

    def get_output_dir(self):
        return "out/" + self.project_name
    
    output_dir = property(get_output_dir)

    def prepare_project(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.output_dir + "/" + self.project_name + ".csproj"):
            os.chdir(self.output_dir)
            os.system("dotnet new classlib")
            os.remove("Class1.cs")
            os.chdir("../..")

        if not os.path.exists("out/" + self._model.name + ".sln"):
            os.chdir("out")
            os.system("dotnet new sln")
            os.rename("out.sln", self._model.name + ".sln")
            os.system("dotnet sln add " + self.project_name + "/" + self.project_name + ".csproj")
            os.chdir("..")

        os.chdir("out")
        os.system("dotnet sln add " + self.project_name + "/" + self.project_name + ".csproj")
        os.chdir("..")

        self.render("BaseEntity.template", "BaseEntity.cs")
    
    def generate_entities(self):
        for entity in self._model.entities:
            self.generate_entity(entity)

    def generate_entity(self, entity):
        self.render("Entity.template", entity.name + ".cs", entity)

    def generate(self):
        self.prepare_project()
        self.generate_entities()

    def __init__(self, model):
        super().__init__(model, "./templates/csharp_model")