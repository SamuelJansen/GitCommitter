import subprocess, time

class GitCommitter:

    def __init__(self,globals):

        self.globals = globals

    def runCommandList(self,commandList):
        for apiName in self.globals.apiNames :
            try :
                for command in commandList :
                    subprocess.call(command, shell=True, cwd=f'C:\\Users\\Samuel Jansen\\Projects\\{apiName}')
            except :
                print(f'[ERROR] {apiName}')

    def addAll(self):
        self.runCommandList([Command.ADD_ALL])

    def commit(self,commitMessage):
        commandCommit = Command.COMMIT.replace(Command.COMMIT_MESSAGE_TOKEN,commitMessage)
        self.runCommandList([commandCommit])

    def push(self):
        self.runCommandList([Command.PUSH])

    def addAllCommitPush(self,commitMessage):
        commandCommit = Command.COMMIT.replace(Command.COMMIT_MESSAGE_TOKEN,commitMessage)
        self.runCommandList([
            Command.ADD_ALL,
            commandCommit,
            Command.PUSH
        ])


class Command:
    GIT_KEYWORD = 'git'

    COMMIT_MESSAGE_TOKEN = '__COMMIT_MESSAGE_TOKEN__'

    ADD_ALL = f'{GIT_KEYWORD} add .'
    COMMIT = f'{GIT_KEYWORD} commit -m "{COMMIT_MESSAGE_TOKEN}"'
    PUSH = f'{GIT_KEYWORD} push'
