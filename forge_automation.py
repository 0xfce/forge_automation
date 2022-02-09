import os, requests as req
from pyunpack import Archive as arch
from argparse import ArgumentParser as argparser

parser = argparser()

parser.add_argument('-p', '--path', help='Project path.', type=str, required=True)
parser.add_argument('-i', '--ide', help='Specify the ide (eclipse/intellij)', type=str, required=False, default='eclipse')
parser.add_argument('-e', '--enviroment', help='Work enviroment (forge/spigot)', type=str, required=False, default='forge')
parser.add_argument('-c', '--clean', help='Clean the project from junk files', action='store_true', required=False)
parser.add_argument('-v', '--version', help='Project version.', default='1.8.9', required=False)
parser.add_argument('-l', '--log', help='Printing steps.', action='store_true', required=False)
parser.add_argument('-b', '--build', help='Create the build.bat file.', action='store_true', required=False)

args = parser.parse_args()

class Color: #taken from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ForgeProject:
    
    mdk_url = 'https://maven.minecraftforge.net/net/minecraftforge/forge/1.8.9-11.15.1.2318-1.8.9/forge-1.8.9-11.15.1.2318-1.8.9-mdk.zip'
    gradle_raw = 'https://pastebin.com/raw/6GWk7S0H'
    gralde_properties_raw = 'https://pastebin.com/raw/BxWUWLt8'
    home_user = os.path.expanduser('~')

    def __init__(this, path:str, version:str='1.8.9', log:bool=True, clean:bool=True, build:bool=True, ide:str='eclipse'):
        this.path = path
        this.version = version
        this.log = log
        this.clean = clean
        this.build = build
        this.ide = ide

    def setup_project(this):
        if not os.path.exists(this.path):
            this.download_and_extract_mdk()
        else:
            print('This project already exists.', Color.FAIL)

    def download_and_extract_mdk(this):
        os.mkdir(this.path)
        url = this.mdk_url if this.version == '1.8.9' else ''
        open('%s/MDK_1.8.9.rar' % (this.path), 'wb').write(req.get(url=url, allow_redirects=False).content)
        this.Log('MDK downloaded.', Color.OKGREEN)
        arch('%s/MDK_1.8.9.rar' % (this.path)).extractall(this.path)
        this.Log('MDK_1.8.9.rar extracted.', Color.OKGREEN)

        try:
            if this.clean:
                this.Log('Cleaning process started...', Color.OKGREEN)
                for file in os.listdir(this.path):
                    if file.endswith('.txt') or file.endswith('.rar'):
                        this.Log('-> %s has been deleted.' % (file), Color.OKCYAN)
                        os.remove(f'{this.path}/{file}')
                this.Log('Cleaning process finished.', Color.OKGREEN)
        except FileNotFoundError:
            pass
        
        if os.path.exists('%s/build.gradle' % (this.path)):
            with open('%s/build.gradle' % (this.path), 'w') as gradle:
                for line in req.get(this.gradle_raw).text:
                    if line != '\n':
                        gradle.write(line)
                gradle.close()
        else:
            raise FileNotFoundError
        this.Log('build.gradle modified.', Color.OKGREEN)
        
        if os.path.exists('%s/gradle/wrapper/gradle-wrapper.properties' % (this.path)):
            with open('%s/gradle/wrapper/gradle-wrapper.properties' % (this.path), 'w') as properties:
                for line in req.get(this.gralde_properties_raw).text:
                    if line != '\n':
                        properties.write(line)
                properties.close()
        else:
            raise FileNotFoundError
        this.Log('gradle-wrapper.properties modified.', Color.OKGREEN)

        os.chdir(this.path)
        os.system('powershell.exe set GRADLE_OPTS=-Xmx4G')
        if not os.path.exists(f'{this.home_user}/.gradle/caches/minecraft/net/minecraftforge/forge/1.8.9-11.15.1.2318-1.8.9/'):
            this.Log('forge %s binaries not found.' % (this.version), Color.WARNING)
            os.system('powershell.exe ./gradlew %s setupDecompWorkspace' % (this.ide))

        os.system('powershell.exe ./gradlew %s clean build' % (this.ide))
        this.Log('gradle process is done.', Color.OKGREEN)
        
        if this.build:
            with open('build.bat', 'x') as build:
                build.write('powershell.exe ./gradlew build\npause')
                build.close()
            this.Log('build.bat created.', Color.OKGREEN)

        this.Log('ur good to go ;).', Color.HEADER)

    def Log(this, msg, color:Color):
        if this.log:
            print('=>', f'{color}{msg}{Color.ENDC}')


if __name__ == '__main__':
    if args.enviroment == 'forge':
        f_project = ForgeProject(args.path, args.version, args.log, args.clean, args.build, args.ide)
        f_project.setup_project()
    else:
        print('at the moment Forge(1.8.9) is the only supported enviroment.')
