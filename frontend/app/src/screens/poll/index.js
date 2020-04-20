import React, { useEffect, useState } from 'react'
import { useParams } from "react-router-dom";

import { currentUser } from '../../utils/auth'
import { getPoll } from '../../crud/poll'
import PollNavBar from '../../components/pollNavBar'
import PollSideBar from '../../components/pollSideBar'


import './styles.css'


const Poll = () => {
    const [ws, setWs] = useState(null)
    const [poll, setPoll] = useState(null)
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    let { slug } = useParams()

    const getCurrentUser = async () => {
        const usr = await currentUser()
        setUser(usr)
        setLoading(false)
    }

    const fetchPollData = async () => {
        const { data } = await getPoll(slug)
        console.log('poll', data);
        setPoll(data)
    }

    if (ws) {
        ws.onmessage = (message) => {
            const data = JSON.parse(message.data)
            if (data.type === "poll_update") {
                setPoll(data)
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
                    <div className="chatView border border-4 border-primary">
                        <div>
                            <p>{user.username}</p>
                            <button onClick={() => ws.send(JSON.stringify({
                                    "message": "React Message",
                                    "username": user.username
                                })
                            )}>
                                Send Message
                            </button>
                        </div>
                    </div>
                    <div className="sideBar border border-2 border-primary">
                        <div>Hey</div>
                    </div>

                </div>
            </div>
        </div>
    )
}

export default Poll
