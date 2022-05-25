from asyncio import subprocess
import yaml
import os
import subprocess
import re

GET_VERSION_COMMAND = "mvn -B help:evaluate -Dexpression=project.version -pl . | grep -v '^\['"
file_name = input("Enter the config file you would like to use, or blank for config.yaml: ")
if file_name == "":
    file_name = "config.yaml"
CONFIG_FILE = open(file_name)
yaml_file = yaml.safe_load(CONFIG_FILE)
keys = list(yaml_file.keys())
previous_component = {}

# Steps
# 1. Update the version of the component
# 2. Build the project
# 3. Get the new version of current component

build_command = ""
print("What command would you like to use to build. Pick one of the following or enter your own command")
print("1. mvn clean install -DskipTests -e")
print("2. mvn clean install -e")
print("3. mvn clean install -DallTests -fae -e")
user_input = input()
if user_input == "1":
    build_command = "mvn clean install -DskipTests -e"
elif user_input == "2":
    build_command = "mvn clean install -e"
elif user_input == "3":
    build_command = "mvn clean install -DallTests -fae -e"
else:
    build_command = user_input
print("Will build with:", build_command)

for project in yaml_file:
    print("Project:", project)
    print("Directory:", yaml_file[project]["directory"])

    os.chdir(yaml_file[project]["directory"])

    if previous_component != {}:
        # update version of project
        component_name = previous_component["component"]
        component_version = previous_component["version"]
        print(f"Writing version {component_version} for <{component_name}>")
        text_file = open("pom.xml", "r")
        data = text_file.read()
        text_file.close()
        data = re.sub(f"(?<=<{component_name}>)(.*)(?=</{component_name}>)", component_version, data, 1)
        text_file = open("pom.xml", "w")
        text_file.write(data)
        text_file.close()

        previous_component = {}

    output = subprocess.getoutput(build_command)
    build_log = open(f"{project}-build.log", "w")
    build_log.write(output)
    build_log.close()

    # If resulted in error
    if "[ERROR]" in output[-100:]:
        print(f"[ERROR] Building {project} failed. Check {project}-build.log in {project} directory to get full logs")
        break
    version = subprocess.check_output(GET_VERSION_COMMAND, shell=True)[:-1].decode("ascii")
    if project != keys[-1]:
        # Update component name and version for next build
        previous_component["component"] = "version." + yaml_file[project]["component"]
        previous_component["version"] = version
