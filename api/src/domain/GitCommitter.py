import subprocess, time

class GitCommitter:

    def __init__(self,globals):

        self.globals = globals

    def runCommand(self,command):
        # try :
            for api in self.globals.apiNames :
                # process = subprocess.Popen('git')
                process = subprocess.call(['git', 'add', '.'], shell=True, cwd='C:\\Users\\Samuel Jansen\\Projects\\GitCommiter')
                time.sleep(20)
                # process = subprocess.Popen(command)
                # process.wait()
                # process.kill()
        # except :
        #     pass

    def addAll(self):
        command = ''
        self.runCommand(command)


class Command:
    ADD_ALL = 'add .'
