if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)

    import sys

    import GitCommitter

    gitCommitter = GitCommitter.GitCommitter(globals)
    gitCommiterCallCommand = sys.argv[1]
    command = sys.argv[2]

    if globals.GIT_COMMITTER == gitCommiterCallCommand :

        if command == GitCommitter.COMMAND_ADD_ENVIRONMENT_VARIABLE :
            gitCommitter.addEnvironmentVariable()

        elif command == GitCommitter.COMMAND_ADD_ALL :
            gitCommitter.addAll()
        elif command == GitCommitter.COMMAND_COMMIT :
            gitCommitter.commit()
        elif command == GitCommitter.COMMAND_PUSH :
            gitCommitter.push()
        elif command == GitCommitter.COMMAND_ADD_ALL_COMMIT_PUSH :
            gitCommitter.addAllCommitPush()

        else :
            print(f'{globals.ERROR}command not fount')
