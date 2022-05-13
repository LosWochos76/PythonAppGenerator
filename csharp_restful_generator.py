from pathlib import Path
import os
from base_generator import BaseGenerator

class CsharpRestfulGenerator(BaseGenerator):
    def get_project_name(self):
        return self._model.name + ".Restful"
    
    project_name = property(get_project_name)

    def get_output_dir(self):
        return "out/" + self.project_name
    
    output_dir = property(get_output_dir)

    def prepare_project(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.output_dir + "/" + self.project_name + ".csproj"):
            os.chdir(self.output_dir)
            os.system("dotnet new webapi")
            os.chdir("../..")
        
        if os.path.exists(self.output_dir + "/WeatherForecast.cs"):
            os.remove(self.output_dir + "/WeatherForecast.cs")
        
        if os.path.exists(self.output_dir + "/Controllers/WeatherForecastController.cs"):
            os.remove(self.output_dir + "/Controllers/WeatherForecastController.cs")

        if not os.path.exists("out/" + self._model.name + ".sln"):
            os.chdir("out")
            os.system("dotnet new sln")
            os.rename("out.sln", self._model.name + ".sln")
            os.system("dotnet sln add " + self.project_name + "/" + self.project_name + ".csproj")
            os.chdir("..")

        os.chdir("out")
        os.system("dotnet sln add " + self.project_name + "/" + self.project_name + ".csproj")
        os.chdir(self.project_name)
        os.system("dotnet add reference ../" + self._model.name + ".Model/" + self._model.name + ".Model.csproj")
        os.system("dotnet add reference ../" + self._model.name + ".Business/" + self._model.name + ".Business.csproj")
        os.chdir("../..")
    
    def generate_controller(self,entity):
        self.render("Controller.template", "Controllers/" + entity.name + "Controller.cs", entity)
    
    def generate_controllers(self):
        for entity in self._model.entities:
            self.generate_controller(entity)
    
    def generate_program(self):
        self.render("Program.template", "Program.cs")

    def generate(self):
        self.prepare_project()
        self.generate_controllers()
        self.generate_program()
    
    def __init__(self, model):
        super().__init__(model, "./templates/csharp_restful")
