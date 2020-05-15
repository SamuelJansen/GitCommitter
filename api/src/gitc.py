import sys

if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = True)
    import GitCommitter
    gitCommitter = GitCommitter.GitCommitter(globals)
    gitCommitter.handleSystemCommand(sys.argv[1:])
