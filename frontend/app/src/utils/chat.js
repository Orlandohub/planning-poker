import {
    createTask,
    allowVotes,
    disallowVotes,
    closeTask,
    vote
} from '../crud/poll'

const OPEN_TASK_CMD = '/open task'
const ALLOW_VOTES_CMD = '/open votes'
const DISALLOW_VOTES_CMD = '/close votes'
const CLOSE_TASK_CMD = '/close task'
const VOTE_CMD = '/vote'

export const slashCmdList = [
    OPEN_TASK_CMD,
    ALLOW_VOTES_CMD,
    DISALLOW_VOTES_CMD,
    CLOSE_TASK_CMD,
    VOTE_CMD
]

export const slashCommandsRouter = {
    [OPEN_TASK_CMD]: createTask,
    [ALLOW_VOTES_CMD]: allowVotes,
    [DISALLOW_VOTES_CMD]: disallowVotes,
    [CLOSE_TASK_CMD]: closeTask,
    [VOTE_CMD]: vote
}

export const slashCommand = (message) => {
    const match = slashCmdList.find((cmd) => {
        const reString = "^\\" + cmd
        const slashCommandRegExp = new RegExp(reString)
        return message.match(slashCommandRegExp)
    })

    return match
}