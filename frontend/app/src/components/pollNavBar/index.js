import React from 'react'
import PropTypes from 'prop-types'
import { Link, useHistory, useParams } from "react-router-dom";
import { useCookies } from 'react-cookie';

import { logout } from '../../utils/auth'


const PollNavBar = ({ws, user}) => {
    const [cookies, removeCookie] = useCookies(['name'])
    let history = useHistory()
    let { slug } = useParams()

    return (
        <nav className="border split-nav">
          <div className="nav-brand">
            <h3>
                <Link to="/poll/home">
                    <span role="img" aria-label="Joker">🃏</span>
                    Planning Poker
                    <span role="img" aria-label="Joker">🃏</span>
                </Link>
                - {user.username} @ {slug}
            </h3>
          </div>
          <div className="collapsible">
            <input id="collapsible1" type="checkbox" name="collapsible1" />
            <button>
            <label htmlFor="collapsible1">
                <div className="bar1"></div>
                <div className="bar2"></div>
                <div className="bar3"></div>
              </label>
            </button>
            <div className="collapsible-body">
              <ul className="inline">
                <li>
                    <button onClick={() => logout(history, removeCookie, ws)}>Logout</button>
                </li>
              </ul>
            </div>
          </div>
        </nav>
    )
}


PollNavBar.propTypes = {
    ws: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired
}

export default PollNavBar
