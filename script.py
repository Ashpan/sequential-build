from asyncio import subprocess
import yaml
import os
import xml.etree.ElementTree as ET
import subprocess

GET_VERSION_COMMAND ="mvn -B help:evaluate -Dexpression=project.version -pl . | grep -v '^\['"
XMLNS = "{http://maven.apache.org/POM/4.0.0}"
CONFIG_FILE = open('config.yaml')
yaml_file = yaml.safe_load(CONFIG_FILE)
keys = list(yaml_file.keys())
previous_component = {}


# Steps
# 1. Update the version of the component
# 2. Build the project
# 3. Get the new version of current component

for project in yaml_file:
    print("Project:", project)
    print("Directory:", yaml_file[project]["directory"])
    
    os.chdir(yaml_file[project]["directory"])
    
    if (previous_component != {}):
        # update version of project
        component_name = previous_component["component"]
        component_version = previous_component["version"]
        root = ET.parse("pom.xml").getroot()
        element = root.find(f".//{XMLNS}{component_name}")
        print(element.text) # Current version on pom.xml
        element.text = component_version
        # Need to save this new one to xml file
        previous_component = {}

    # subprocess.getoutput("mvn clean install -DskipTests -e") TODO: Un-comment
    version = subprocess.check_output(GET_VERSION_COMMAND, shell=True)[:-1].decode("ascii")
    if (project != keys[-1]):
        previous_component["component"] = "version." + yaml_file[project]["component"]
        previous_component["version"] = version
