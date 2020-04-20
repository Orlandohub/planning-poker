import React, { useState, useRef } from 'react'
import { useHistory } from 'react-router-dom'
import slugify from 'slugify'

import { createPoll } from '../../crud/poll'


const CreatePollModal = () => {
    const [pollName, setPollName] = useState("")
    const inputEl = useRef(null);
    const history = useHistory()

    const createPollAndNavigate = async (pollName) => {
        const response = await createPoll(pollName)
        if (response && response.status === 200) {
            history.push(`/poll/${slugify(pollName)}`)
        }
        inputEl.current.checked = false
    }

    return (
        <div>
            <label className="paper-btn" htmlFor="modal-2">Create Poll</label>
            <input ref={inputEl} className="modal-state" id="modal-2" type="checkbox" />
            <div className="modal">
                <label className="modal-bg" htmlFor="modal-2"></label>
                <div className="modal-body">
                    <label className="btn-close" htmlFor="modal-2">X</label>
                    <h4 className="modal-title">Poll Name</h4>
                    <div className="form-group">
                        <input
                            onChange={(e) => {setPollName(e.target.value)}}
                            value={pollName}
                            type="text" 
                            placeholder="Poll Name"
                            id="paperInputs1"
                        />
                    </div>
                    <button htmlFor="modal-2" onClick={() => createPollAndNavigate(pollName)}>Create</button>
                </div>
            </div>
        </div>
    )
}


export default CreatePollModal