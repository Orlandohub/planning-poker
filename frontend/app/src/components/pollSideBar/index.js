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

    const active_users = (poll && poll.active_users) || []
    const votes = (poll && poll.current_task && poll.current_task.votes) || {}
    const displayVotes = poll && poll.current_task && poll.current_task.allow_votes
    const user_included = active_users.includes(user.username)
    console.log('votes', votes);

    return (
        <div className="sideBar border border-2 border-primary">
            <div>
                
                    
                {
                    Object.keys(votes).length > 0 ?
                    <React.Fragment>
                        <p>
                            <b>Votes&nbsp;</b>
                            <span className="badge success">
                                {Object.keys(votes).length}
                            </span>
                        </p>
                        <div className="userList">
                            { Object.keys(votes).map((username, key) => 
                                {
                                    return (
                                        <div key={key}>
                                            {username} {
                                                !displayVotes ?
                                                <kbd>{votes[username]}</kbd>
                                                :
                                                <span role="img" aria-label="Vote">🎴</span>
                                            }
                                        </div>
                                    )
                                }
                            )}
                        </div>
                    </React.Fragment> :
                    <React.Fragment>
                        <p>
                            <b>Users&nbsp;</b>
                            <span className="badge primary">
                                {
                                    user_included ?
                                    active_users.length :
                                    active_users.length + 1
                                }
                            </span>
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
                    </React.Fragment>

                }
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