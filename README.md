# Sequential Maven Build Tool

## Config File

To use this sequential build tool you will need `Python 3` and `pip` installed.
Then run the following command to install dependencies.
```shell
python -m pip install -r requirements.txt
```
> **_NOTE:_** Optionally you could also create a venv for this project by running `python -m venv env` and access python from `env/bin/python` instead of just `python` from your PATH

You will then need to make a `config.yaml` file, you can change the filename but will have to specify so every time you run this script.
The file should be of the following format, also seen in the `example-config.yaml`
```yaml
WildFly-Elytron:
    directory: /home/user/workspace/elytron
    component: org.wildfly.security.elytron
WildFly-Core:
    directory: /home/user/workspace/core
    component: org.wildfly.core
WildFly:
    directory: /home/user/workspace/wildfly
```
This file specifies that you want to build projects in the following order: `WildFly-Elytron`, `WildFly-Core`, and finally `WildFly`.
It will first build the project (based on the command you specify during the execution of the script) and then go to the next project, and modify the version of the  `component` from the previous project in its `pom.xml`.

For example: After building `WildFly-Elytron` it will open `/home/user/workspace/core/pom.xml`, find the version for the component `org.wildfly.security.elytron` and modify it with the new SNAPSHOT version created when builing `Elytron`. This will also happen with WildFly as well.

## Script Execution
To start the script, run the following command
```shell
python script.py
```
1. You will first be prompted with
```
Enter the config file you would like to use, or blank for config.yaml: 
```
If you named your configuration file something other than `config.yaml` specify that now.

2. Next it will ask what build command you would like to use
```
What command would you like to use to build. Pick one of the following or enter your own command
1. mvn clean install -DskipTests -e
2. mvn clean install -e
3. mvn clean install -DallTests -fae -e
```
You can either use a preset defined, or specify your own build command

3. The script will execute the sequential build and should print out useful logging information. The output of each build will be saved to `%directory%/%project%-build.log` from each project specified in the yaml configuration.
