import subprocess, codecs

import gitc

class Command:

    KW_GIT = 'git'
    KW_SELF = 'self'
    KW_CLONE = 'clone'
    KW_STATUS = 'status'
    KW_BRANCH = 'branch'
    KW_PULL = 'pull'
    KW_CHECKOUT = 'checkout'
    KW_ADD = 'add'
    KW_COMMIT = 'commit'
    KW_PUSH = 'push'

    TOKEN_REPOSITORY_URL = '__TOKEN_REPOSITORY_URL__'
    TOKEN_COMMIT_MESSAGE = '__TOKEN_COMMIT_MESSAGE__'
    TOKEN_BRANCH_NAME = '__TOKEN_BRANCH_NAME__'

    CLONE = f'{KW_GIT} {KW_CLONE} {TOKEN_REPOSITORY_URL}'
    STATUS = f'{KW_GIT} {KW_STATUS}'
    BRANCH = f'{KW_GIT} {KW_BRANCH}'
    PULL = f'{KW_GIT} {KW_PULL}'
    CHECKOUT = f'{KW_GIT} {KW_CHECKOUT} {TOKEN_BRANCH_NAME}'
    CHECKOUT_DASH_B = f'{KW_GIT} {KW_CHECKOUT} -b {TOKEN_BRANCH_NAME}'
    ADD = f'{KW_GIT} {KW_ADD} .'
    COMMIT = f'{KW_GIT} {KW_COMMIT} -m "{TOKEN_COMMIT_MESSAGE}"'
    PUSH = f'{KW_GIT} {KW_PUSH}'


KW_ALL = 'all'
KW_IF_DASH_NEEDED = 'if-needed'

COMMAND_CLONE_ALL_IF_NEEDED = f'{Command.KW_CLONE}-{KW_ALL}-{KW_IF_DASH_NEEDED}'
COMMAND_CHECKOUT_B_ALL_IF_NEEDED = f'{Command.KW_CHECKOUT}-b-{KW_ALL}-{KW_IF_DASH_NEEDED}'

COMMAND_STATUS_ALL = f'{Command.KW_STATUS}-{KW_ALL}'
COMMAND_BRANCH_ALL = f'{Command.KW_BRANCH}-{KW_ALL}'
COMMAND_PULL_ALL = f'{Command.KW_PULL}-{KW_ALL}'
COMMAND_CHECKOUT_ALL = f'{Command.KW_CHECKOUT}-{KW_ALL}'
COMMAND_ADD_ALL = f'{Command.KW_ADD}-{KW_ALL}'
COMMAND_COMMIT_ALL = f'{Command.KW_COMMIT}-{KW_ALL}'
COMMAND_PUSH_ALL = f'{Command.KW_PUSH}-{KW_ALL}'
COMMAND_ADD_COMMIT_PUSH_ALL = f'{Command.KW_ADD}-{Command.KW_COMMIT}-{Command.KW_PUSH}-{KW_ALL}'
COMMAND_ADD_ENVIRONMENT_VARIABLE = f'add-environment-variable'

class GitCommitter:

    GIT_COMMITTER_INDEX = 0
    COMMAND_INDEX = 1
    _1_ARGUMENT_INDEX = 2
    _2_ARGUMENT_INDEX = 3

    def runCommandList(self,commandList):
        globals = self.globals
        returnSet = {}
        for apiName in globals.apiNameList :
            try :
                returnSet[apiName] = {}
                for command in commandList :
                    print(f'{globals.NEW_LINE}[{apiName}] {command}')
                    processPath = f'{globals.localPath}{globals.apisRoot}{apiName}'
                    returnSet[apiName][command] = subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
                    print(self.getProcessReturnValue(returnSet[apiName][command]))
                    self.globals.debug(returnSet[apiName][command])
            except Exception as exception :
                print(f'{self.globals.ERROR}{apiName}{globals.SPACE_DASH_SPACE}{command}{globals.NEW_LINE}{str(exception)}')
        return returnSet

    def runApiNameCommandListTree(self,apiNameCommandListTree):
        globals = self.globals
        for apiName,commandList in apiNameCommandListTree.items() :
            try :
                for command in commandList :
                    print(f'{globals.NEW_LINE}[{apiName}] {command}')
                    subprocess.call(command, shell=True, cwd=f'{globals.localPath}{globals.apisRoot}')
            except Exception as exception :
                print(f'{self.globals.ERROR}{apiName}{globals.SPACE_DASH_SPACE}{command}{globals.NEW_LINE}{str(exception)}')

    def __init__(self,globals):

        self.GIT_COMMITTER = globals.GIT_COMMITTER

        self.globals = globals
        self.gitUrl = globals.getApiSetting(f'api.git.url')
        self.gitExtension = globals.getApiSetting(f'api.git.extension')
        self.commandSet = {
            COMMAND_ADD_ENVIRONMENT_VARIABLE : self.addEnvironmentVariable,

            COMMAND_CLONE_ALL_IF_NEEDED : self.cloneAllIfNeeded,
            COMMAND_CHECKOUT_B_ALL_IF_NEEDED : self.checkoutBAllIfNeeded,

            COMMAND_STATUS_ALL : self.statusAll,
            COMMAND_BRANCH_ALL : self.branchAll,
            COMMAND_PULL_ALL : self.pullAll,
            COMMAND_CHECKOUT_ALL : self.checkoutAll,
            COMMAND_ADD_ALL : self.addAll,
            COMMAND_COMMIT_ALL : self.commitAll,
            COMMAND_PUSH_ALL : self.pushAll,
            COMMAND_ADD_COMMIT_PUSH_ALL : self.addCommitPushAll
        }

    def cloneAllIfNeeded(self,sysCommandList):
        globals = self.globals
        repositoryNameList = list(globals.getPathTreeFromPath(f'{globals.localPath}{globals.apisRoot}').keys())
        apiNameCommandListTree = {}
        for apiName in globals.apiNameList :
            if apiName not in repositoryNameList :
                repositoryUrl = f'{self.gitUrl}{apiName}.{self.gitExtension}'
                command = Command.CLONE.replace(Command.TOKEN_REPOSITORY_URL,repositoryUrl)
                apiNameCommandListTree[apiName] = [command]
        self.runApiNameCommandListTree(apiNameCommandListTree)

    def checkoutBAllIfNeeded(self,sysCommandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',sysCommandList)
        commandCheckoutAll = Command.CHECKOUT.replace(Command.TOKEN_BRANCH_NAME,branchName)
        returnSet = self.runCommandList([commandCheckoutAll])
        if returnSet and returnSet.items():
            for apiName,specificReturnSet in returnSet.items() :
                if specificReturnSet and specificReturnSet.items() :
                    for key,value in specificReturnSet.items() :
                        if 'error' in self.getProcessReturnErrorValue(value) :
                            command = CHECKOUT_DASH_B.replace(TOKEN_BRANCH_NAME,branchName)
                            apiNameCommandListTree = {apiName:[command]}
                            self.runApiNameCommandListTree(apiNameCommandListTree)
        self.debugReturnSet('checkoutBAllIfNeeded',self.getReturnSetValue(returnSet))

    def statusAll(self,sysCommandList):
        returnSet = self.runCommandList([Command.STATUS])
        self.debugReturnSet('statusAll',self.getReturnSetValue(returnSet))

    def branchAll(self,sysCommandList):
        returnSet = self.runCommandList([Command.BRANCH])
        self.debugReturnSet('branchAll',self.getReturnSetValue(returnSet))

    def pullAll(self,sysCommandList):
        returnSet = self.runCommandList([Command.PULL])
        self.debugReturnSet('pullAll',self.getReturnSetValue(returnSet))

    def checkoutAll(self,sysCommandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',sysCommandList)
        commandCheckoutAll = Command.CHECKOUT.replace(Command.TOKEN_BRANCH_NAME,branchName)
        returnSet = self.runCommandList([commandCheckoutAll])
        self.debugReturnSet('checkoutAll',self.getReturnSetValue(returnSet))


    def addAll(self,sysCommandList):
        returnSet = self.runCommandList([Command.ADD])
        self.debugReturnSet('addAll',self.getReturnSetValue(returnSet))

    def commitAll(self,sysCommandList):
        commitMessage = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Commit message',sysCommandList)
        commandCommit = Command.COMMIT.replace(Command.TOKEN_COMMIT_MESSAGE,commitMessage)
        returnSet = self.runCommandList([commandCommit])
        self.debugReturnSet('commitAll',self.getReturnSetValue(returnSet))

    def pushAll(self,sysCommandList):
        returnSet = self.runCommandList([Command.PUSH])
        self.debugReturnSet('pushAll',self.getReturnSetValue(returnSet))

    def addCommitPushAll(self,sysCommandList):
        commitMessage = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Commit message',sysCommandList)
        commandCommit = Command.COMMIT.replace(Command.TOKEN_COMMIT_MESSAGE,commitMessage)
        returnSet = self.runCommandList([
            Command.ADD,
            commandCommit,
            Command.PUSH
        ])
        self.debugReturnSet('addCommitPushAll',self.getReturnSetValue(returnSet))

    def addEnvironmentVariable(self,sysCommandList):
        variableKey = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Environment variable key',sysCommandList)
        variableValue = self.getArg(GitCommitter._2_ARGUMENT_INDEX,'Environment variable value',sysCommandList)
        globals = self.globals
        if variableKey == Command.KW_SELF :
            variableValue = f'{globals.localPath}{globals.apisRoot}{GitCommitter.__name__}{globals.BACK_SLASH}{globals.baseApiPath}'
            print(variableValue)
        os.environ[variableKey] = variableValue

    def handleSystemCommand(self,sysCommandList):
        sysCommandList = sysCommandList.copy()
        globals = self.globals
        MISSING_SPACE = 'Missing '
        if len(sysCommandList) == 0 or globals.GIT_COMMITTER not in sysCommandList :
            print(f'{globals.ERROR}{MISSING_SPACE}{globals.DOUBLE_QUOTE}{globals.GIT_COMMITTER}{globals.DOUBLE_QUOTE}')
            return
        if len(sysCommandList) < self.COMMAND_INDEX :
            print(f'{globals.ERROR}{MISSING_SPACE}{globals.GIT_COMMITTER} command')
            return
        gitCommiterCallCommand = sysCommandList[self.GIT_COMMITTER_INDEX]
        command = sysCommandList[self.COMMAND_INDEX]
        if globals.GIT_COMMITTER == gitCommiterCallCommand :
            try :
                self.commandSet[command](sysCommandList)
            except :
                print(f'{globals.ERROR}command not fount')

    def getProcessReturnValue(self,processReturn):
        return str(processReturn.stdout,self.globals.ENCODING)

    def getProcessReturnErrorValue(self,processReturn):
        return str(processReturn.stderr,self.globals.ENCODING)

    def getReturnSetValue(self,returnSet):
        globals = self.globals
        returnValue = globals.NOTHING
        if returnSet and returnSet.items():
            for apiName,specificReturnSet in returnSet.items() :
                if specificReturnSet and specificReturnSet.items() :
                    for key,value in specificReturnSet.items() :
                        processReturnValue = self.getProcessReturnValue(value)
                        if processReturnValue and not globals.NOTHING == processReturnValue :
                            returnValue += f'{apiName}{globals.SPACE_DASH_SPACE}{key}{globals.NEW_LINE}{processReturnValue}'
                        else :
                            returnValue += f'{apiName}{globals.SPACE_DASH_SPACE}{key}{globals.NEW_LINE}{self.getProcessReturnErrorValue(value)}'
                    returnValue += globals.NEW_LINE
        return returnValue

    def printReturn(self,processReturn):
        print(self.getReturnValue(processReturn))

    def debugReturnSet(self,callMethodName,ReturnSetValue):
        self.globals.debug(f'{callMethodName}{2 * self.globals.NEW_LINE}{ReturnSetValue}')

    def getArg(self,argIndex,typingGetMessage,sysCommandList) :
        try :
            if '()' in sysCommandList[argIndex] :
                return self.getImput(typingGetMessage)
            return sysCommandList[argIndex]
        except :
            return self.getImput(typingGetMessage)

    def getImput(self,typingGetMessage):
        return input(f'{typingGetMessage}{self.globals.COLON_SPACE}')
