if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)

    import sys
    commitMessage = sys.argv[1]

    import GitCommitter

    gitCommitter = GitCommitter.GitCommitter(globals)
    gitCommitter.addAllCommitPush(commitMessage)
