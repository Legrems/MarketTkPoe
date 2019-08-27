import wget
import requests
import json
import zipfile
import os


GIT_URL = "https://api.github.com/repos/Legrems/MarketTkPoe/releases"
DWN_URL = "https://www.github.com/Legrems/MarketTkPoe/archive/"


class PackageInstaller():

    def __init__(self):
        self.command = "python -m pip {}"
        self.package = []

    def install(self, package):
        os.system(self.command.format(package))

    def install_all(self):
        for p in self.packages:
            self.install(p)


class Updater():

    def __init__(self):
        self.version = ''
        self.releases = {}
        self.filepath = 'temp.zip'
        self.destination_folder = './'

    @property
    def is_up_to_date(self):
        return self.version == self.latest_version

    @property
    def latest_version(self):
        self.getUpdates()

        return self.releases[-1]['tag_name']

    @property
    def actual_version(self):
        for file in os.listdir():
            if os.path.isdir(file):
                for subfile in os.listdir(file):
                    if subfile == 'main.py':
                        self.version = file[12:]
        return self.version

    def getUpdates(self):
        self.releases = json.loads(requests.get(GIT_URL).text)

    def update(self):
        if self.is_up_to_date:
            return

        release_url = DWN_URL + self.latest_version + '.zip'

        try:
            wget.download(release_url, self.filepath)
        except:
            print('Cannot download from git, please contact an admin :)')

        zp = zipfile.ZipFile(self.filepath, 'r')
        zp.extractall(self.destination_folder)

        os.remove(self.filepath)

    def list_releases(self):
        for r in self.releases:
            print(r['tag_name'])

    def launch_app(self):
        self.update()
        os.system(f"python MarketTkPoe-{self.actual_version}/main.py")


up = Updater()
up.launch_app()
