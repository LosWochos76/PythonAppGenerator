from pathlib import Path
import os
from base_generator import BaseGenerator

class CsharpBusinessGenerator(BaseGenerator):
    def get_project_name(self):
        return self._model.name + ".Business"
    
    project_name = property(get_project_name)

    def get_output_dir(self):
        return "out/" + self.project_name
    
    output_dir = property(get_output_dir)

    def prepare_project(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir + "/Filters").mkdir(parents=True, exist_ok=True)
        Path(self.output_dir + "/Services").mkdir(parents=True, exist_ok=True)

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
        
        self.render("BaseFilter.template", "Filters/BaseFilter.cs")
        
        os.chdir("out")
        os.system("dotnet sln add " + self.project_name + "/" + self.project_name + ".csproj")
        os.chdir(self.project_name)
        os.system("dotnet add reference ../" + self._model.name + ".Model/" + self._model.name + ".Model.csproj")
        os.system("dotnet add reference ../" + self._model.name + ".Persistence/" + self._model.name + ".Persistence.csproj")
        os.chdir("../..")

    def generate_services(self):
        for entity in self._model.entities:
            self.render("Service.template", "Services/" + entity.name + "Service.cs", entity)
            self.render("Filter.template", "Filters/" + entity.name + "Fiter.cs", entity)

    def generate(self):
        self.prepare_project()
        self.generate_services()
    
    def __init__(self, model):
        super().__init__(model, "./templates/csharp_business")
