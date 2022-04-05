import os, subprocess, requests as req
from pyunpack import Archive as arch
from argparse import ArgumentParser as argparser

parser = argparser()

parser.add_argument('-p', '--path', help='Project path.', type=str, required=True)
parser.add_argument('-i', '--ide', help='Specify the ide (eclipse/intellij)', type=str, required=False, default='eclipse')
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
    _1_8_9 = 'https://maven.minecraftforge.net/net/minecraftforge/forge/1.8.9-11.15.1.2318-1.8.9/forge-1.8.9-11.15.1.2318-1.8.9-mdk.zip'
    _1_9_4 = 'https://maven.minecraftforge.net/net/minecraftforge/forge/1.9.4-12.17.0.2317-1.9.4/forge-1.9.4-12.17.0.2317-1.9.4-mdk.zip'
    _1_12_2 = 'https://maven.minecraftforge.net/net/minecraftforge/forge/1.12.2-14.23.5.2859/forge-1.12.2-14.23.5.2859-mdk.zip'

    _1_8_gradle_raw = 'https://pastebin.com/raw/6GWk7S0H'
    _1_9_gradle_raw = 'https://pastebin.com/raw/axm5xEzp'
    _1_12_gradle_raw = 'https://pastebin.com/raw/CA1K4aSF'
    gralde_properties_raw = 'https://pastebin.com/raw/BxWUWLt8'
    java_version = subprocess.Popen(['java', '-version'], stdin=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1]
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
            if '1.8.0_' in str(this.java_version, 'utf-8'):
                try:
                    java_home = os.environ['JAVA_HOME']
                    if 'jdk' in java_home:
                        this.download_and_extract_mdk()
                    elif 'jre' in java_home:
                        print(Color.FAIL, 'Please point the JAVA_HOME to JDK not jre.')
                except KeyError:
                    print(Color.FAIL, 'JAVA_HOME not found.', Color.ENDC)
            else:
                print(Color.FAIL, 'Please set the java path to 1.8.0', Color.ENDC)
        else:
            print(Color.FAIL,'This project already exists.', Color.ENDC)

    def download_and_extract_mdk(this):
        os.mkdir(this.path)
        url = this._1_8_9 if this.version == '1.8.9' or this.version == '1.8' else this._1_9_4 if this.version == '1.9' or this.version == '1.9.4' else this._1_12_2 if this.version == '1.12' or this.version == '1.12.2' else this._1_8_9
        binaries = '1.9.4-12.17.0.2317-1.9.4' if this.version == '1.9' or this.version == '1.9.4' else '1.8.9-11.15.1.2318-1.8.9' if this.version == '1.8' or this.version == '1.8.9' else '1.12.2-14.23.5.2859' if this.version == '1.12' or this.version == '1.12.2' else '1.8.9-11.15.1.2318-1.8.9'
        this.Log('Downloading %s from %s' % (this.version, url), Color.HEADER)
        open('%s/MDK_%s.rar' % (this.path, this.version), 'wb').write(req.get(url=url, allow_redirects=False).content)
        this.Log('MDK_%s downloaded.'%(this.version), Color.OKGREEN)
        arch('%s/MDK_%s.rar' % (this.path, this.version)).extractall(this.path)
        this.Log('MDK_%s.rar extracted.'%(this.version), Color.OKGREEN)

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
                for line in req.get(this._1_8_gradle_raw if this.version == '1.8' or this.version == '1.8.9' else this._1_9_gradle_raw if this.version == '1.9' or this.version == '1.9.4' else this._1_12_gradle_raw if this.version == '1.12' or this.version == '1.12.2' else this._1_8_gradle_raw).text:
                    if line != '\n':
                        gradle.write(line)
                gradle.close()
        else:
            this.Log('build.gradle not found', Color.FAIL)
        this.Log('build.gradle modified.', Color.OKGREEN)

        if os.path.exists('%s/gradle/wrapper/gradle-wrapper.properties' % (this.path)):
            with open('%s/gradle/wrapper/gradle-wrapper.properties' % (this.path), 'w') as properties:
                for line in req.get(this.gralde_properties_raw).text:
                    if line != '\n':
                        properties.write(line)
                properties.close()
        else:
            this.Log('gradle-wrapper.properties not found.', Color.FAIL)
        this.Log('gradle-wrapper.properties modified.', Color.OKGREEN)

        os.chdir(this.path)
        os.system('powershell.exe set GRADLE_OPTS=-Xmx4G')

        if not os.path.exists(f'{this.home_user}/.gradle/caches/minecraft/net/minecraftforge/forge/{binaries}/'):
            this.Log('forge %s binaries not found.' % (this.version), Color.WARNING)
            this.Log('%sExecuting setupDecompWorkspace for %s binaries.' % ( Color.BOLD, binaries), Color.WARNING)
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
    ForgeProject(args.path, args.version, args.log, args.clean, args.build, args.ide).setup_project()
