import React, {useState} from 'react'
import PropTypes from 'prop-types'

import ChatMessage from '../chatMessage'
import {
    slashCommandsRouter,
    slashCommand
} from '../../utils/chat'

import './styles.css'


const Chat = ({
    setMessages,
    messages,
    ws,
    user,
    slug,
    poll
}) => {
    const [message, setMessage] = useState("")

    const handleChange = (e) => {
        setMessage(e.target.value)
    }

    const handleKeyDown = async (e) => {
        const { username } = user
        const sent_date = new Date()
        if (e.key === "Enter") {
            e.preventDefault()
            // On message submit check for slash commands.
            // If slash command, trigger action and reply
            // server response only to the user who submited the cmd
            const slashCmdMatch = slashCommand(message)
            if (slashCmdMatch) {
                // Remove slash command from message
                const rawMessage = message.replace(slashCmdMatch, "")
                const task = poll.current_task
                // Call function for slash command
                const response = await slashCommandsRouter[slashCmdMatch](rawMessage, slug, task)
                // Send Message to cmd issuer
                if (response && response.message) {
                    const resMsg = {
                        username: "Planning Poker",
                        message: response.message,
                        sent_date: sent_date
                    }
                    setMessages([resMsg, ...messages])
                }
            } else {
                // If no slash command, submit message via websocket
                ws.send(JSON.stringify({username, message, sent_date}))
            }
            // Finally clear the message
            setMessage("")
        }
    }

    messages.sort((a, b) => {
        return new Date(b.sent_date) - new Date(a.sent_date)
    })

    return (
        <div className="chatContainer">
            <div className="chatView border border-4 border-primary">
                {
                    messages.map((data, key) =>
                        <ChatMessage data={data} key={key} />
                    )
                }
            </div>
            <div className="chatInput">
                <div className="form-group">
                    <textarea
                        onChange={handleChange}
                        onKeyDown={handleKeyDown}
                        value={message}
                        className="no-resize"
                        placeholder="Type Message Here">
                    </textarea>
                </div>
            </div>
        </div>
    )
}


Chat.propTypes = {
    messages: PropTypes.array.isRequired,
    ws: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired,
    slug: PropTypes.string.isRequired,
    setMessages: PropTypes.func.isRequired,
    poll: PropTypes.object
}

export default Chat
