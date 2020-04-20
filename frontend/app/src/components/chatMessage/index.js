import React from 'react'
import PropTypes from 'prop-types'

import './styles.css'

const ChatMessage = ({data}) => {
    const { username, message, sent_date } = data
    const sentAt = new Date(sent_date)
    const hours = sentAt.getHours()
    const minutes = sentAt.getMinutes()

    return (
        <div>
            <div className="messageContainer">
                <div className="avatar">
                    <img src='https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Round&hatColor=PastelOrange&hairColor=BrownDark&facialHairType=MoustacheFancy&facialHairColor=BrownDark&clotheType=ShirtVNeck&clotheColor=Gray01&eyeType=Hearts&eyebrowType=FlatNatural&mouthType=Concerned&skinColor=Light'
                    />
                </div>
                <div className="message">
                    <p className="messageHeader"><b>{username}</b> @ <small>{hours}:{minutes}</small></p>
                    <p>{message}</p>
                </div>
            </div>
        </div>

    )
}


ChatMessage.propTypes = {
    data: PropTypes.object.isRequired
}


export default ChatMessage
