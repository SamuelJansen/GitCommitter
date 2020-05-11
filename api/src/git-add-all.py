if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)

    import GitCommitter

    gitCommitter = GitCommitter.GitCommitter(globals)
    gitCommitter.addAll()
