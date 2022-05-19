from asyncio import subprocess
import yaml
import subprocess

CONFIG_FILE = open('config.yaml')
yaml_file = yaml.safe_load(CONFIG_FILE)
for project in yaml_file:
    print("Project:", project)
    print("Directory", yaml_file[project]["directory"])
    get_version_command ="$(mvn -B help:evaluate -Dexpression=project.version -pl . | grep -v '^\[')"
    cd_command = subprocess.run("cd %s" % yaml_file[project]["directory"], shell=True, capture_output=True)
    version = subprocess.run(get_version_command, shell=True, capture_output=True)
    print(version)
# cd 