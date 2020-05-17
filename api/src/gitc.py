def gitCommitter(commandList,globals,**kwargs):
    import GitCommitter
    gitCommitter = GitCommitter.GitCommitter(globals,**kwargs)
    gitCommitter.handleCommandList(commandList)

if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)
    import SystemHelper
    SystemHelper.run(gitCommitter,globals)
