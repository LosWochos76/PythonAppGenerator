from pathlib import Path
import os
from base_generator import BaseGenerator

class AngularGenerator(BaseGenerator):
    def get_project_name(self):
        return self._model.name + ".Backend"
    
    project_name = property(get_project_name)

    def get_output_dir(self):
        return "out/" + self.project_name
    
    output_dir = property(get_output_dir)

    def prepare_project(self):
        os.chdir("out")
        os.system("ng new " + self._model.name + " --directory " + self.project_name + " --routing true --style css --strict false")
        os.chdir(self.project_name)
        os.system("ng add @angular/material --defaults --interactive false --skip-confirmation true")
        os.system("ng generate @angular/material:navigation misc/NavigationBar --defaults")
        os.chdir("../..")
        Path(self.output_dir + "/src/app/model").mkdir(parents=True, exist_ok=True)
        Path(self.output_dir + "/src/app/services").mkdir(parents=True, exist_ok=True)
        Path(self.output_dir + "/src/app/misc").mkdir(parents=True, exist_ok=True)

    def generate_single_files(self):
        self.render("app_component.html.template", "src/app/app.component.html")
        self.render("app-routing.module.ts.template", "src/app/app-routing.module.ts")
        self.render("navigation-bar.component.html.template", "src/app/misc/navigation-bar/navigation-bar.component.html")
        self.render("logging.service.ts.template", "src/app/services/logging.service.ts")
        self.render("app.module.ts.template", "src/app/app.module.ts")
        self.render("environment.ts.template", "src/environments/environment.ts")
        self.render("environment.prod.ts.template", "src/environments/environment.prod.ts")

    def generate_entity(self,entity):
        os.chdir(self.output_dir)
        os.system("ng generate component " + 
            entity.name.lower() + "/" + entity.name + "List --defaults")
        os.system("ng generate component " + 
            entity.name.lower() + "/" + entity.name + "Edit --defaults")
        os.chdir("../..")
        self.render("entity.ts.template", "src/app/model/" + entity.name.lower() + ".ts", entity)
        self.render("service.ts.template", "src/app/services/" + entity.name.lower() + ".service.ts", entity)
        self.render("list.component.ts.template", "src/app/" + entity.name.lower() + "/" + entity.name.lower() + "-list/" + entity.name.lower() + "-list.component.ts", entity)
        self.render("list.component.html.template", "src/app/" + entity.name.lower() + "/" + entity.name.lower() + "-list/" + entity.name.lower() + "-list.component.html", entity)
        self.render("list.component.css.template", "src/app/" + entity.name.lower() + "/" + entity.name.lower() + "-list/" + entity.name.lower() + "-list.component.css", entity)
        self.render("edit.component.html.template", "src/app/" + entity.name.lower() + "/" + entity.name.lower() + "-edit/" + entity.name.lower() + "-edit.component.html", entity)

    def generate_entities(self):
        for entity in self._model.entities:
            self.generate_entity(entity)

    def generate(self):
        self.prepare_project()
        self.generate_single_files()
        self.generate_entities()
    
    def __init__(self, model):
        super().__init__(model, "./templates/angular")
