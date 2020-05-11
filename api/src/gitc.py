def handleSystemCommand(gitCommitter) :

    import sys

    import GitCommitter

    globals = gitCommitter.globals

    if len(sys.argv) <= gitCommitter._0_ or globals.GIT_COMMITTER not in sys.argv :
        print(f'{globals.ERROR}Missing "git-commiter"')
        return
    if len(sys.argv) < gitCommitter._2_ITS_RESERVED_FOR_COMMAND :
        print(f'{globals.ERROR}Missing git-commiter command')
        return

    gitCommiterCallCommand = sys.argv[gitCommitter._1_ITS_RESERVED_FOR_GIT_COMMITTER]
    command = sys.argv[gitCommitter._2_ITS_RESERVED_FOR_COMMAND]

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


if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)

    import GitCommitter

    gitCommitter = GitCommitter.GitCommitter(globals)

    handleSystemCommand(gitCommitter)
