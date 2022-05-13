#!/Users/stuckenholz/anaconda3/bin/python
from model import Model
import os

from csharp_model_generator import CsharpModelGenerator
from csharp_persistence_generator import CsharpPersistenceGenerator
from csharp_business_generator import CsharpBusinessGenerator
from csharp_restful_generator import CsharpRestfulGenerator
from angular_generator import AngularGenerator

#if os.path.isdir("out"):
#    print("Removing old output...")
#    os.system("rm -rf out")

model = Model()

model_generator = CsharpModelGenerator(model)
model_generator.generate()

persistence_generator = CsharpPersistenceGenerator(model)
persistence_generator.generate()

business_generator = CsharpBusinessGenerator(model)
business_generator.generate()

restful_generator = CsharpRestfulGenerator(model)
restful_generator.generate()

angular_generator = AngularGenerator(model)
angular_generator.generate()
