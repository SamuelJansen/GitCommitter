import Levenshtein

import VoiceAssistant

VoiceAssistant = VoiceAssistant.VoiceAssistant

def run(gitCommitter) :
    globals = gitCommitter.globals
    voiceAssistant = gitCommitter.voiceAssistant
    voiceAssistant.awake = True
    globals = voiceAssistant.globals

    selectedCommand = None
    gitCommitterResponseList = []
    while voiceAssistant.awake :
        content = voiceAssistant.listen()
        if content not in VoiceAssistant.SLEEP :
            if selectedCommand and content in gitCommitter.CONFIRM :
                response = gitCommitter.handleCommandList([globals.GIT_COMMITTER,selectedCommand])
                gitCommitterResponseList.append(response)
            else :
                selectedCommand = None
                voiceAssistant.speak(content)
                gradedCommandSet = {}
                for command in gitCommitter.commandSet.keys() :
                    commandScore = Levenshtein.distance(content,globals.SPACE.join(command.split(globals.DASH)))
                    if gradedCommandSet.get(commandScore) :
                        gradedCommandSet[commandScore].append(command)
                    else :
                        gradedCommandSet[commandScore] = [command]
                selectedSortedCommand = sorted(gradedCommandSet.items())
                selectedCommand = selectedSortedCommand[0][1][0]
                print(f'{globals.GIT_COMMITTER} {selectedCommand}')
        elif content in VoiceAssistant.SLEEP :
            voiceAssistant.awake = False
    return gitCommitterResponseList
