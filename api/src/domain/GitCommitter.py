import os, subprocess, time

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

    def addEnvironmentVariable(self,variableKey,variableValue):
        globals = self.globals
        if variableKey == Command.KW_SELF :
            variableValue = f'{globals.localPath}{globals.apisRoot}{GitCommitter.__name__}{globals.BACK_SLASH}{globals.baseApiPath}'
            print(variableValue)
        os.environ[variableKey] = variableValue


class Command:
    KW_GIT = 'git'
    KW_SELF = 'self'

    COMMIT_MESSAGE_TOKEN = '__COMMIT_MESSAGE_TOKEN__'

    ADD_ALL = f'{KW_GIT} add .'
    COMMIT = f'{KW_GIT} commit -m "{COMMIT_MESSAGE_TOKEN}"'
    PUSH = f'{KW_GIT} push'
