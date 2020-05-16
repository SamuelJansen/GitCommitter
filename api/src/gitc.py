import sys

def run(globals):
    import GitCommitter
    gitCommitter = GitCommitter.GitCommitter(globals)
    gitCommitter.handleCommandList(sys.argv[1:])

if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = True)
    try :
        import SystemHelper
        systemHelper = SystemHelper.SystemHelper(globals)
        systemHelper.handleSystemArgumentValue(sys.argv,run)
    except :
        run(globals)
