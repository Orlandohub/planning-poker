import React, { useEffect, useState } from 'react'
import { useCookies } from 'react-cookie';
import { useHistory, useParams } from "react-router-dom";

import { currentUser, logout } from '../../utils/auth'


const Poll = () => {
    const [ws, setWs] = useState()
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [cookies, removeCookie] = useCookies(['name'])

    let { slug } = useParams()
    let history = useHistory();

    const getCurrentUser = async () => {
        const usr = await currentUser()
        setUser(usr)
        setLoading(false)
    }

    if (ws) {
        ws.onmessage = (message) => { console.log(message) }
        ws.onclose = (message) => { console.log(message) }
    }

    useEffect(() => {
        getCurrentUser()
        setWs(new WebSocket(`ws://localhost:8000/poll/${slug}/chat`))
    }, [])

    if (loading) {
        return null
    }
    return (
        <div>
            <p>{user.username}</p>
            <button onClick={() => ws.send(JSON.stringify({
                            "message": "React Message",
                            "username": user.username
                        }))}>Send Message</button>
            <button onClick={() => logout(history, removeCookie, ws)}>logout</button>
        </div>
    )
}

export default Poll
