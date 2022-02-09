# Forge Automation
Just a simple forge projects automation, this will automatically download the latest forge-1.8.9-mdk and extract it into a project and run all the commands needed to make a forge project. im too lazy D: !
## Installation
First of all, you have to download some libraries
```sh
pip install pyunpack
```
```sh
pip install requests
```

## How to use
- -p/--path: Project path. (Required)
- -i/--ide: Specify the ide (eclipse/intellij). (default arg value is eclipse)
- -e/--enviroment: Work enviroment (forge/spigot). (default arg value is forge)
- -c/--clean: Delete the license files from the project.
- -l/--log: Printing the steps from downloading to the last event.
- -b/--build: Creates the build.bat file for you.
```sh
python forge_automation.py -p F:/development/java/forge/YourProjectNameHere/ -cbl
```

## Note
- You must have python3 & pip already installed on your computer
- This script only for 1.8.9 forge
- FOR WINDOWS ONLY!
