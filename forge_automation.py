import sys
import os
import requests as req
from pyunpack import Archive as arch

arg1 = sys.argv[1]
arg2 = sys.argv[2]

mdk_url = 'https://maven.minecraftforge.net/net/minecraftforge/forge/1.8.9-11.15.1.2318-1.8.9/forge-1.8.9-11.15.1.2318-1.8.9-mdk.zip'
gradle_raw = 'https://pastebin.com/raw/ZHDdUXjg'
gralde_properties_raw = 'https://pastebin.com/raw/BxWUWLt8'

if arg1 == 'eclipse' or arg1 == 'idea':
    if os.path.exists(arg2):
        print('this project already exist in the followin directory')
    else:
        os.mkdir(arg2)

        open(f'{arg2}/1.8.9-mdk.rar', 'wb').write(req.get(url=mdk_url, allow_redirects=True).content)

        print('forge 1.8.9 mdk downloaded, extractin...')

        arch(f'{arg2}/1.8.9-mdk.rar').extractall(arg2)

        print('forge 1.8.9 mdk extracted, cleanin directory...')

        for file in os.listdir(path=arg2):
            if file.endswith('.txt') or file.endswith('.rar'):
                os.remove(f'{arg2}/{file}')

        print('directory cleaned, modifyin build.gradle...')

        os.chdir(arg2)

        if os.path.exists('build.gradle'):
            gradle = open('build.gradle', 'w')
            for line in req.get(gradle_raw).text:
                if line != '\n':
                    gradle.write(line)
            gradle.close()

        print('build.gradle modified, modifyin wrapper...')

        if os.path.exists('gradle/wrapper/gradle-wrapper.properties'):
            properties = open('gradle/wrapper/gradle-wrapper.properties', 'w')
            for line in req.get(gralde_properties_raw).text:
                if line != '\n':
                    properties.write(line)
            properties.close()

        print('wrapper modified, startin gradle...')

        os.system(f'powershell.exe ./gradlew {arg1} clean build')

        print('gradle finished its job, creatin bat file to build your mod...')

        build = open('build.bat', 'x')
        build.write('powershell.exe .\gradlew build\npause')
        build.close()

        print('build.bat created.')

        print('you\'re good to go ;).')

else:
    print('ide not found')




