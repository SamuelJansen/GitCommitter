import os, sys, subprocess, time

import gitc

COMMAND_CLONE_ALL_IF_NEEDED = 'clone-all-if-needed'
COMMAND_PULL_ALL = 'pull-all'
COMMAND_CHECKOUT_ALL = 'checkout-all'
COMMAND_ADD_ALL = 'add-all'
COMMAND_COMMIT = 'commit'
COMMAND_PUSH = 'push'
COMMAND_ADD_ALL_COMMIT_PUSH = 'add-commit-push-all'
COMMAND_ADD_ENVIRONMENT_VARIABLE = 'add-environment-variable'

class GitCommitter:

    def __init__(self,globals):
        self.globals = globals
        self._1_ITS_RESERVED_FOR_GIT_COMMITTER = 1
        self._2_ITS_RESERVED_FOR_COMMAND = 2
        self._3_ = 3

        self.gitUrl = globals.getSetting(f'{globals.apiName}.api.git.url')
        self.gitExtension = globals.getSetting(f'{globals.apiName}.api.git.extension')
        print(f'globals.settingTree = {globals.settingTree}')
        print(f'globals.apiName = {globals.apiName}')
        print(f'gitUrl = {self.gitUrl}, gitExtension = {self.gitExtension}')

    def runCommandList(self,commandList):
        globals = self.globals
        for apiName in globals.apiNameList :
            try :
                for command in commandList :
                    print(f'{globals.NEW_LINE}[{apiName}] {command}')
                    subprocess.call(command, shell=True, cwd=f'{globals.localPath}{globals.apisRoot}{apiName}')
            except :
                print(f'{self.globals.ERROR}{apiName}{globals.SPACE_HIFEN_SPACE}{command}')

    def runApiNameCommandListTree(self,apiNameCommandListTree):
        globals = self.globals
        for apiName,commandList in apiNameCommandListTree.items() :
            try :
                for command in commandList :
                    print(f'{globals.NEW_LINE}[{apiName}] {command}')
                    subprocess.call(command, shell=True, cwd=f'{globals.localPath}{globals.apisRoot}')
            except :
                print(f'{self.globals.ERROR}{apiName}{globals.SPACE_HIFEN_SPACE}{command}')

    def cloneAllIfNeeded(self):
        globals = self.globals
        repositoryNameList = list(globals.getPathTreeFromPath(f'{globals.localPath}{globals.apisRoot}').keys())
        apiNameCommandListTree = {}
        for apiName in globals.apiNameList :
            if apiName not in repositoryNameList :
                repositoryUrl = f'{self.gitUrl}{apiName}.{self.gitExtension}'
                commandCloneAllIfNeeded = Command.CLONE.replace(Command.TOKEN_REPOSITORY_URL,repositoryUrl)
                apiNameCommandListTree[apiName] = [commandCloneAllIfNeeded]
        self.runApiNameCommandListTree(apiNameCommandListTree)

    def pullAll(self):
        self.runCommandList([Command.PULL_ALL])

    def checkoutAll(self):
        branchName = sys.argv[self._3_]
        commandCheckoutAll = Command.CHECKOUT_ALL.replace(Command.TOKEN_BRANCH_NAME,branchName)
        self.runCommandList([commandCheckoutAll])

    def addAll(self):
        self.runCommandList([Command.ADD_ALL])

    def commitAll(self):
        commitMessage = sys.argv[self._2_ITS_RESERVED_FOR_COMMAND]
        commandCommit = Command.COMMIT.replace(Command.TOKEN_COMMIT_MESSAGE,commitMessage)
        self.runCommandList([commandCommit])

    def pushAll(self):
        self.runCommandList([Command.PUSH])

    def addCommitPushAll(self):
        commitMessage = sys.argv[self._2_ITS_RESERVED_FOR_COMMAND]
        commandCommit = Command.COMMIT.replace(Command.TOKEN_COMMIT_MESSAGE,commitMessage)
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

    TOKEN_REPOSITORY_URL = '__TOKEN_REPOSITORY_URL__'
    TOKEN_COMMIT_MESSAGE = '__TOKEN_COMMIT_MESSAGE__'
    TOKEN_BRANCH_NAME = '__TOKEN_BRANCH_NAME__'

    CLONE = f'{KW_GIT} clone {TOKEN_REPOSITORY_URL}'
    PULL_ALL = f'{KW_GIT} pull'
    CHECKOUT_ALL = f'{KW_GIT} checkout {TOKEN_BRANCH_NAME}'
    ADD_ALL = f'{KW_GIT} add .'
    COMMIT = f'{KW_GIT} commit -m "{TOKEN_COMMIT_MESSAGE}"'
    PUSH = f'{KW_GIT} push'
