from cmath import inf
import sys
from model import Model
from pathlib import Path
import os
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

class BaseGenerator:
    _model = any
    _env = any

    def fetch_output_from_template(self,infile,entity=None):
        template = self._env.get_template(infile)

        if entity:
            return template.render(model=self._model, entity=entity)
        else:
            return template.render(model=self._model)

    def render(self,infile,outfile,entity=None):
        output = self.fetch_output_from_template(infile,entity)
        with open(self.output_dir + "/" + outfile, "w") as fh:
            fh.write(output)
    
    def replace_in_file(self,infile,outfile,replace_string,entity=None):
        output = self.render(infile,entity)
        fin = open(self.template_dir + "/" + outfile, "rt")
        data = fin.read()
        data = data.replace(replace_string, output)
        fin.close()
        fin = open(self.template_dir + "/" + outfile, "wt")
        fin.write(data)
        fin.close() 
    
    def __init__(self, model, template_dir):
        print("Generating model-project for c#...")
        self._model = model
        self._env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(),
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<<%',
            variable_end_string='%>>',
            comment_start_string='<#',
            comment_end_string='#>',
            trim_blocks=True,
            lstrip_blocks=True
        )