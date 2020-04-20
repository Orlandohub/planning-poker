import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { Link, useParams } from 'react-router-dom'

import CreatePollModal from '../createPollModal'
import { getAll } from '../../crud/poll'

import './styles.css'


const PollSideBar = ({poll, user}) => {
    const [pollList, setPollList] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    let { slug } = useParams()


    const getPollList = async () => {
        const res = await getAll()
        setPollList(res.data)
        setIsLoading(false)
    }

    useEffect(() => {
        getPollList()
    }, [slug])

    if (isLoading) {
        return null
    }

    const active_users = (poll && poll.active_users && poll.active_users) || []
    const user_included = active_users.includes(user.username)

    return (
        <div className="sideBar border border-2 border-primary">
            <div className="activeUsers">
                <p>
                    <b>
                        Users&nbsp;
                        <span className="badge primary">
                            {
                                user_included ?
                                active_users.length :
                                active_users.length + 1
                            }
                        </span>
                    </b>
                </p>
                <div className="userList">
                    <div>{user.username}</div>
                    { active_users.map((username, key) => 
                        {
                            if (user.username !== username) {
                                return <div key={key}>{username}</div>
                            }
                            return null
                        }
                    )}
                </div>
            </div>
            <div className="pollListContainer">
                <p><b>Polls <span className="badge secondary">{pollList.length}</span></b></p>
                <div className="pollList">
                    {
                        pollList.map((poll, key) => 
                            <div key={key}>
                                <Link to={`/poll/${poll.slug}`}>{poll.name}</Link>
                            </div>
                        )
                    }
                </div>
                <CreatePollModal />
            </div>
        </div>
    )
}


PollSideBar.propTypes = {
    poll: PropTypes.object,
    user: PropTypes.object.isRequired
}


export default PollSideBar