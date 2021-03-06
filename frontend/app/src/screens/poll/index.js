import React, { useEffect, useState } from 'react'
import { useParams } from "react-router-dom";

import { currentUser } from '../../utils/auth'
import { getPoll } from '../../crud/poll'
import PollNavBar from '../../components/pollNavBar'
import PollSideBar from '../../components/pollSideBar'
import TaskSideBar from '../../components/taskSideBar'
import Chat from '../../components/chat'


import './styles.css'


const Poll = () => {
    const [ws, setWs] = useState(null)
    const [poll, setPoll] = useState(null)
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [messages, setMessages] = useState([])

    let { slug } = useParams()

    const getCurrentUser = async () => {
        const usr = await currentUser()
        setUser(usr)
        setLoading(false)
    }

    const fetchPollData = async () => {
        const { data } = await getPoll(slug)
        setPoll(data)
        const messages = (data && data.chat && data.chat.messages) || []
        setMessages(messages)
    }

    if (ws) {
        ws.onmessage = (message) => {
            const data = JSON.parse(message.data)
            if (data.type === "poll_update") {
                setPoll(data)
            }
            if (data.type === "message") {
                setMessages([data.message, ...messages])
            }
        }
            
        ws.onclose = (message) => { console.log(message) }
        ws.onopen = (message) => { }
    }

    useEffect(() => {
        if (!user) {
            getCurrentUser()
        }
        // When moving from one room to another
        // need to disconnect previous websocket
        if (ws) {
            ws.close()
        }
        setWs(new WebSocket(`ws://localhost:8000/poll/${slug}/chat`))
        fetchPollData()
    }, [slug])

    if (loading) {
        return null
    }
    return (
        <div>
            <PollNavBar ws={ws} user={user} />
            <div className="pollContainer">
                <div className="pollWindow">
                    <PollSideBar poll={poll} user={user} />
                    <Chat
                        user={user}
                        ws={ws}
                        messages={messages}
                        slug={slug}
                        setMessages={setMessages}
                        poll={poll}
                    />
                    <TaskSideBar poll={poll} />
                </div>
            </div>
        </div>
    )
}

export default Poll
