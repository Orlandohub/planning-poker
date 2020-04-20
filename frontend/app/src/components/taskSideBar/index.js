import React from 'react'
import PropTypes from 'prop-types'


import './styles.css'


const TaskSideBar = ({ poll }) => {
    const currentTask = poll && poll.current_task
    let voteState = ""
    let badge = ""

    if (currentTask && currentTask.allow_votes) {
        voteState = "Vote"
        badge = "success"
    } else if (currentTask) {
        voteState = "Votes Closed"
    }

    return (
        <div className="sideBar border border-4 border-primary">
            <div className="taskContainer">
                <p>
                    <b>
                        Task&nbsp;
                        {
                            currentTask ?
                                <span className={`badge ${badge}`}> {voteState}</span> :
                                null

                        }
                    </b>
                </p>
                <div className="taskDescription">
                    <div className="papper">
                        <p className="taskText">
                            {
                                currentTask ?
                                    currentTask.description :
                                    "No Task At The Moment!"
                            }
                        </p>
                    </div>
                </div>
            </div>
            <div className="taskContainer taskDescription">
                <p><b>Slash Command List:</b></p>

                <pre className="commandList">
                    <code>
                        /open task {"<task-name>"} <br/>
                        /close task <br/>
                        /open votes <br/>
                        /close votes <br/>
                        /vote {'<vote>'}
                    </code>
                </pre>
                <p><b>Possible Votes:</b></p>
                <div>
                    <kbd>0</kbd>&nbsp;
                    <kbd>1/2</kbd>&nbsp;
                    <kbd>1</kbd>&nbsp;
                    <kbd>2</kbd>&nbsp;
                    <kbd>3</kbd>&nbsp;
                    <kbd>5</kbd>&nbsp;
                    <kbd>8</kbd>&nbsp;
                    <kbd>13</kbd>&nbsp;                    
                </div>

            </div>
        </div>
    )
}


TaskSideBar.propTypes = {
    poll: PropTypes.object
}

export default TaskSideBar
