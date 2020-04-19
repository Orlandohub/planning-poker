import React, { useEffect, useState } from 'react'
import { useHistory } from "react-router-dom";

import { currentUser, logout } from '../../utils/auth'


const Poll = () => {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    let history = useHistory();

    const getCurrentUser = async () => {
        const usr = await currentUser()
        setUser(usr)
        setLoading(false)
    }

    useEffect(() => {
        getCurrentUser()
    }, [])

    if (loading) {
        return null
    }
    return (
        <div>
            <p>{user.username}</p>
            <button onClick={() => logout(history)}>logout</button>
        </div>
    )
}

export default Poll
