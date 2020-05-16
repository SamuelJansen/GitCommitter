import Levenshtein

import VoiceAssistant

VoiceAssistant = VoiceAssistant.VoiceAssistant

def run(gitCommitter) :
    globals = gitCommitter.globals
    voiceAssistant = gitCommitter.voiceAssistant
    voiceAssistant.awake = True
    globals = voiceAssistant.globals

    selectedCommand = None
    while voiceAssistant.awake :
        content = voiceAssistant.listen()
        if content not in VoiceAssistant.SLEEP :
            if selectedCommand and content in gitCommitter.CONFIRM :
                gitCommitter.handleCommandList([globals.GITC_GIT_COMMITTER,selectedCommand[0][1][0]])
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
                selectedCommand = sorted(gradedCommandSet.items())
                globals.debug(f'{globals.GITC_GIT_COMMITTER} {selectedCommand[0][1][0]}')
        elif content in VoiceAssistant.SLEEP :
            voiceAssistant.awake = False
    return selectedCommand
