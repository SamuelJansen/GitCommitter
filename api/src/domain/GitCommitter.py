import os, sys, subprocess, time

import gitc

COMMAND_ADD_ALL = 'add-all'
COMMAND_COMMIT = 'commit'
COMMAND_PUSH = 'push'
COMMAND_ADD_ALL_COMMIT_PUSH = 'add-all-commit-push'
COMMAND_ADD_ENVIRONMENT_VARIABLE = 'add-environment-variable'

class GitCommitter:

    def __init__(self,globals):

        self.globals = globals
        self._0_ = 0
        self._1_ITS_RESERVED_FOR_GIT_COMMITTER = 1
        self._2_ITS_RESERVED_FOR_COMMAND = 2
        self._3_ = 3

    def runCommandList(self,commandList):
        globals = self.globals
        for apiName in globals.apiNameList :
            try :
                for command in commandList :
                    subprocess.call(command, shell=True, cwd=f'{globals.localPath}{globals.apisRoot}{apiName}')
            except :
                print(f'{self.globals.ERROR}{apiName}')

    def addAll(self):
        self.runCommandList([Command.ADD_ALL])

    def commit(self):
        commitMessage = sys.argv[self._2_ITS_RESERVED_FOR_COMMAND]
        commandCommit = Command.COMMIT.replace(Command.COMMIT_MESSAGE_TOKEN,commitMessage)
        self.runCommandList([commandCommit])

    def push(self):
        self.runCommandList([Command.PUSH])

    def addAllCommitPush(self):
        commitMessage = sys.argv[self._2_ITS_RESERVED_FOR_COMMAND]
        commandCommit = Command.COMMIT.replace(Command.COMMIT_MESSAGE_TOKEN,commitMessage)
        self.runCommandList([
            Command.ADD_ALL,
            commandCommit,
            Command.PUSH
        ])

    def addEnvironmentVariable(self):
        variableKey = sys.argv[self._2_ITS_RESERVED_FOR_COMMAND]
        variableValue = sys.argv[self._3_]
        globals = self.globals
        if variableKey == Command.KW_SELF :
            variableValue = f'{globals.localPath}{globals.apisRoot}{GitCommitter.__name__}{globals.BACK_SLASH}{globals.baseApiPath}'
            print(variableValue)
        os.environ[variableKey] = variableValue

    def handleSystemCommand(self):
        gitc.handleSystemCommand(self)


class Command:
    KW_GIT = 'git'
    KW_SELF = 'self'

    COMMIT_MESSAGE_TOKEN = '__COMMIT_MESSAGE_TOKEN__'

    ADD_ALL = f'{KW_GIT} add .'
    COMMIT = f'{KW_GIT} commit -m "{COMMIT_MESSAGE_TOKEN}"'
    PUSH = f'{KW_GIT} push'
