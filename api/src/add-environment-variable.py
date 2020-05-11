if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)

    import sys
    variableKey = sys.argv[1]
    variableValue = sys.argv[2]

    import GitCommitter

    gitCommitter = GitCommitter.GitCommitter(globals)
    gitCommitter.addEnvironmentVariable(variableKey,variableValue)
