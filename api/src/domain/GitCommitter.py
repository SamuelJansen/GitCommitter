import subprocess, codecs

import gitc, WakeUpVoiceAssistant, VoiceAssistant, GitCommand

GitCommand = GitCommand.GitCommand

class GitCommitter:

    GIT_COMMITTER_INDEX = 0
    COMMAND_INDEX = 1
    _1_ARGUMENT_INDEX = 2
    _2_ARGUMENT_INDEX = 3

    MISSING_SPACE = 'Missing '

    WAKE_UP_VOICE_ASSISTANT = 'voice-assistant'

    KW_ALL = 'all'
    KW_IF_DASH_NEEDED = 'if-needed'
    KW_PROJECT = 'project'

    CLONE_ALL_IF_NEEDED = f'{GitCommand.KW_CLONE}-{KW_ALL}-{KW_IF_DASH_NEEDED}'
    CHECKOUT_B_ALL_IF_NEEDED = f'{GitCommand.KW_CHECKOUT}-b-{KW_ALL}-{KW_IF_DASH_NEEDED}'
    PUSH_SET_UPSTREAM_ORIGIN_BRANCH_IF_NEEDED = f'{GitCommand.KW_PUSH}-set-upstream-{GitCommand.KW_ORIGIN}-{KW_ALL}-{KW_IF_DASH_NEEDED}'

    STATUS_ALL = f'{GitCommand.KW_STATUS}-{KW_ALL}'
    BRANCH_ALL = f'{GitCommand.KW_BRANCH}-{KW_ALL}'
    PULL_ALL = f'{GitCommand.KW_PULL}-{KW_ALL}'
    CHECKOUT_ALL = f'{GitCommand.KW_CHECKOUT}-{KW_ALL}'
    ADD_ALL = f'{GitCommand.KW_ADD}-{KW_ALL}'
    COMMIT_ALL = f'{GitCommand.KW_COMMIT}-{KW_ALL}'
    PUSH_ALL = f'{GitCommand.KW_PUSH}-{KW_ALL}'
    ADD_COMMIT_PUSH_ALL = f'{GitCommand.KW_ADD}-{GitCommand.KW_COMMIT}-{GitCommand.KW_PUSH}-{KW_ALL}'
    MERGE_ORIGIN_ALL = f'{GitCommand.KW_MERGE}-{GitCommand.KW_ORIGIN}-{KW_ALL}'

    CLONE_PROJECT_IF_NEEDED = f'{GitCommand.KW_CLONE}-{KW_PROJECT}-{KW_IF_DASH_NEEDED}'
    ADD_COMMIT_PUSH_PROJECT = f'{GitCommand.KW_ADD}-{GitCommand.KW_COMMIT}-{GitCommand.KW_PUSH}-{KW_PROJECT}'


    ADD_ENVIRONMENT_VARIABLE = f'add-environment-variable'

    SKIP = 'skip'

    CONFIRM = ['execute']

    def handleCommandList(self,sysCommandList):
        globals = self.globals
        if len(sysCommandList) < GitCommitter.COMMAND_INDEX :
            print(f'{globals.ERROR}{GitCommitter.MISSING_SPACE}{globals.GIT_COMMITTER} command')
            return
        gitCommiterCallCommand = sysCommandList[GitCommitter.GIT_COMMITTER_INDEX]
        command = sysCommandList[GitCommitter.COMMAND_INDEX]
        if globals.GIT_COMMITTER == gitCommiterCallCommand :
            try :
                return self.commandSet[command](sysCommandList)
            except Exception as exception :
                print(f'''{globals.ERROR}Error processing command "{gitCommiterCallCommand} {command}": {str(exception)}''')

    def __init__(self,globals):
        self.globals = globals
        self.GIT_COMMITTER = globals.GIT_COMMITTER
        self.gitUrl = globals.getApiSetting(f'api.git.url')
        self.gitExtension = globals.getApiSetting(f'api.git.extension')
        self.commandSet = {
            GitCommitter.WAKE_UP_VOICE_ASSISTANT : self.wakeUpVoiceAssistant,

            GitCommitter.CLONE_ALL_IF_NEEDED : self.cloneAllIfNeeded,
            GitCommitter.CHECKOUT_B_ALL_IF_NEEDED : self.checkoutBAllIfNeeded,
            GitCommitter.PUSH_SET_UPSTREAM_ORIGIN_BRANCH_IF_NEEDED : self.pushSetUpStreamAllIfNedded,

            GitCommitter.STATUS_ALL : self.statusAll,
            GitCommitter.BRANCH_ALL : self.branchAll,
            GitCommitter.PULL_ALL : self.pullAll,
            GitCommitter.CHECKOUT_ALL : self.checkoutAll,
            GitCommitter.ADD_ALL : self.addAll,
            GitCommitter.COMMIT_ALL : self.commitAll,
            GitCommitter.PUSH_ALL : self.pushAll,
            GitCommitter.ADD_COMMIT_PUSH_ALL : self.addCommitPushAll,
            GitCommitter.MERGE_ORIGIN_ALL : self.mergeOriginAll,

            GitCommitter.CLONE_PROJECT_IF_NEEDED : self.cloneProjectIfNeeded,
            GitCommitter.ADD_COMMIT_PUSH_PROJECT : self.addCommitPushProject,

            GitCommitter.ADD_ENVIRONMENT_VARIABLE : self.addEnvironmentVariable
        }

    def runCommandList(self,commandList):
        globals = self.globals
        returnSet = {}
        for projectName in globals.apiNameList :
            try :
                returnSet[projectName] = {}
                for command in commandList :
                    print(f'{globals.NEW_LINE}[{projectName}] {command}')
                    processPath = f'{globals.localPath}{globals.apisRoot}{projectName}'
                    returnSet[projectName][command] = subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
                    print(self.getProcessReturnValue(returnSet[projectName][command]))
                    # globals.debug(returnSet[projectName][command])
            except Exception as exception :
                print(f'{self.globals.ERROR}{projectName}{globals.SPACE_DASH_SPACE}{command}{globals.NEW_LINE}{str(exception)}')
        return returnSet

    def runCommandListTree(self,commandListTree,path=None):
        globals = self.globals
        returnSet = {}
        for projectName,commandList in commandListTree.items() :
            try :
                returnSet[projectName] = {}
                for command in commandList :
                    if path :
                        processPath = path
                    else :
                        processPath = f'{globals.localPath}{globals.apisRoot}{projectName}'
                    print(f'{globals.NEW_LINE}[{projectName}] {command} {processPath}')
                    returnSet[projectName][command] = subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
                    print(self.getProcessReturnValue(returnSet[projectName][command]))
            except Exception as exception :
                print(f'{self.globals.ERROR}{projectName}{globals.SPACE_DASH_SPACE}{command}{globals.NEW_LINE}{str(exception)}')
        return returnSet

    def cloneProjectIfNeeded(self,sysCommandList):
        globals = self.globals
        projectName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Project name',sysCommandList)
        projectNameList = list(globals.getPathTreeFromPath(f'{globals.localPath}{globals.apisRoot}').keys())
        commandListTree = {}
        if not projectNameList or projectName not in projectNameList :
            projectUrl = f'{self.gitUrl}{projectName}.{self.gitExtension}'
            command = GitCommand.CLONE.replace(GitCommand.TOKEN_PROJECT_URL,projectUrl)
            processPath = f'{globals.localPath}{globals.apisRoot}'
            commandListTree[projectName] = [command]
        else :
            print(f'{projectName} already exists')
        if commandListTree :
            returnSet = {}
            returnSet = self.runCommandListTree(commandListTree,path=processPath)
            self.debugReturnSet('cloneProjectIfNeeded',self.getReturnSetValue(returnSet))

    def addCommitPushProject(self,sysCommandList):
        projectName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Project name',sysCommandList)
        commitMessage = self.getArg(GitCommitter._2_ARGUMENT_INDEX,'CommitMessage name',sysCommandList)
        if projectName :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            returnSet = self.runCommandListTree({projectName:[
                GitCommand.ADD,
                commandCommit,
                GitCommand.PUSH
            ]})
            self.debugReturnSet('addCommitPushProject',self.getReturnSetValue(returnSet))

    def cloneAllIfNeeded(self,sysCommandList):
        globals = self.globals
        projectNameList = list(globals.getPathTreeFromPath(f'{globals.localPath}{globals.apisRoot}').keys())
        if projectNameList :
            commandListTree = {}
            for projectName in globals.apiNameList :
                if projectName not in projectNameList :
                    projectUrl = f'{self.gitUrl}{projectName}.{self.gitExtension}'
                    command = GitCommand.CLONE.replace(GitCommand.TOKEN_PROJECT_URL,projectUrl)
                    processPath = f'{globals.localPath}{globals.apisRoot}'
                    commandListTree[projectName] = [command]
                else :
                    print(f'{projectName} already exists')

            if commandListTree :
                returnSet = self.runCommandListTree(commandListTree,path=processPath)
                self.debugReturnSet('cloneAllIfNeeded',self.getReturnSetValue(returnSet))

    def checkoutBAllIfNeeded(self,sysCommandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',sysCommandList)
        if branchName :
            commandCheckoutAll = GitCommand.CHECKOUT.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
            returnSet = self.runCommandList([commandCheckoutAll])
            if returnSet and returnSet.items():
                for projectName,specificReturnSet in returnSet.items() :
                    if specificReturnSet and specificReturnSet.items() :
                        for key,value in specificReturnSet.items() :
                            if 'error' in self.getProcessReturnErrorValue(value) :
                                command = GitCommand.CHECKOUT_DASH_B.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
                                commandListTree = {projectName:[command]}
                                returnCorrectionSet = self.runCommandListTree(commandListTree)
            self.debugReturnSet('checkoutBAllIfNeeded',self.getReturnSetValue(returnSet))

    def pushSetUpStreamAllIfNedded(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.PUSH])
        returnCorrectionSet = {}
        if returnSet and returnSet.items():
            for projectName,specificReturnSet in returnSet.items() :
                returnCorrectionSet[projectName] = {}
                if specificReturnSet and specificReturnSet.items() :
                    for key,value in specificReturnSet.items() :
                        for line in self.getProcessReturnErrorValue(value).split(self.globals.NEW_LINE) :
                            if GitCommand.PUSH_SET_UPSTREAM_ORIGIN in line :
                                commandPush = GitCommand.BRANCH
                                returnCorrectionSet[projectName][commandPush] = self.runCommandListTree({projectName:[commandPush]})[projectName][commandPush]
                                dirtyBranchNameList = self.getProcessReturnValue(returnCorrectionSet[projectName][commandPush]).split(self.globals.NEW_LINE)
                                if dirtyBranchNameList :
                                    for dirtyBranchName in dirtyBranchNameList :
                                        if '*' in dirtyBranchName :
                                            branchName = dirtyBranchName.split()[1].strip()
                                            commandPushSetUpStreamAll = GitCommand.PUSH_SET_UPSTREAM_ORIGIN_BRANCH.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
                                            returnCorrectionSet[projectName][commandPushSetUpStreamAll] = self.runCommandListTree({projectName:[commandPushSetUpStreamAll]})[projectName][commandPushSetUpStreamAll]
        self.debugReturnSet('pushSetUpStreamAllIfNedded',self.getReturnSetValue(returnSet))

    def statusAll(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.STATUS])
        self.debugReturnSet('statusAll',self.getReturnSetValue(returnSet))

    def branchAll(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.BRANCH])
        self.debugReturnSet('branchAll',self.getReturnSetValue(returnSet))

    def fetchAll(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.FETCH])
        self.debugReturnSet('fetchAll',self.getReturnSetValue(returnSet))

    def pullAll(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.PULL])
        self.debugReturnSet('pullAll',self.getReturnSetValue(returnSet))

    def checkoutAll(self,sysCommandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',sysCommandList)
        if branchName :
            commandCheckoutAll = GitCommand.CHECKOUT.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
            returnSet = self.runCommandList([commandCheckoutAll])
            self.debugReturnSet('checkoutAll',self.getReturnSetValue(returnSet))

    def addAll(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.ADD])
        self.debugReturnSet('addAll',self.getReturnSetValue(returnSet))

    def commitAll(self,sysCommandList):
        commitMessage = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Commit message',sysCommandList)
        if commitMessage :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            returnSet = self.runCommandList([commandCommit])
            self.debugReturnSet('commitAll',self.getReturnSetValue(returnSet))

    def pushAll(self,sysCommandList):
        returnSet = self.runCommandList([GitCommand.PUSH])
        self.debugReturnSet('pushAll',self.getReturnSetValue(returnSet))

    def addCommitPushAll(self,sysCommandList):
        commitMessage = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Commit message',sysCommandList)
        if commitMessage :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            returnSet = self.runCommandList([
                GitCommand.ADD,
                commandCommit,
                GitCommand.PUSH
            ])
            self.debugReturnSet('addCommitPushAll',self.getReturnSetValue(returnSet))

    def mergeOriginAll(self,sysCommandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',sysCommandList)
        if branchName :
            commandMergeOriginAll = GitCommand.MERGE_ORIGIN.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
            returnSet = self.runCommandList([commandMergeOriginAll])
            self.debugReturnSet('mergeOriginAll',self.getReturnSetValue(returnSet))

    def addEnvironmentVariable(self,sysCommandList):
        variableKey = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Environment variable key',sysCommandList)
        variableValue = self.getArg(GitCommitter._2_ARGUMENT_INDEX,'Environment variable value',sysCommandList)
        if variableKey and variableValue :
            globals = self.globals
            if variableKey == GitCommand.KW_SELF :
                variableValue = f'{globals.localPath}{globals.apisRoot}{GitCommitter.__name__}{globals.BACK_SLASH}{globals.baseApiPath}'
                print(variableValue)
            os.environ[variableKey] = variableValue

    def wakeUpVoiceAssistant(self,sysCommandList):
        self.voiceAssistant = VoiceAssistant.VoiceAssistant(self.globals)
        WakeUpVoiceAssistant.run(self)

    def getProcessReturnValue(self,processReturn):
        return str(processReturn.stdout,self.globals.ENCODING)

    def getProcessReturnErrorValue(self,processReturn):
        return str(processReturn.stderr,self.globals.ENCODING)

    def getReturnSetValue(self,returnSet):
        globals = self.globals
        returnValue = globals.NOTHING
        if returnSet and returnSet.items():
            for projectName,specificReturnSet in returnSet.items() :
                if specificReturnSet and specificReturnSet.items() :
                    for key,value in specificReturnSet.items() :
                        processReturnValue = self.getProcessReturnValue(value)
                        if processReturnValue and not globals.NOTHING == processReturnValue :
                            returnValue += f'{projectName}{globals.SPACE_DASH_SPACE}{key}{globals.NEW_LINE}{processReturnValue}'
                        else :
                            returnValue += f'{projectName}{globals.SPACE_DASH_SPACE}{key}{globals.NEW_LINE}{self.getProcessReturnErrorValue(value)}'
                    returnValue += globals.NEW_LINE
        return returnValue

    def printReturn(self,processReturn):
        print(self.getReturnValue(processReturn))

    def debugReturnSet(self,callMethodName,ReturnSetValue):
        self.globals.debug(f'{callMethodName}{2 * self.globals.NEW_LINE}{ReturnSetValue}')

    def getArg(self,argIndex,typingGetMessage,sysCommandList) :
        try :
            if '()' in sysCommandList[argIndex] :
                return self.validInput(self.getImput(typingGetMessage))
            return sysCommandList[argIndex]
        except Exception as exception :
            self.globals.debug(f'Not possible to get sysCommandList[{argIndex}]. Cause: {str(exception)}')
            return self.validInput(self.getImput(typingGetMessage))

    def validInput(self,input):
        if input == GitCommitter.SKIP :
            return None
        else :
            return input

    def getImput(self,typingGetMessage):
        return input(f'{typingGetMessage}{self.globals.COLON_SPACE}')
