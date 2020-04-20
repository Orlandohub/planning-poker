import axios from 'axios'


export const createPoll = async (name) => {
    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return response
    }

    console.log('name', name);
    console.log('token_bearer', token_bearer);


    response = await axios.post(
        'http://localhost:8000/poll/create',
        JSON.stringify({ name: name }),
        {
            headers: {
              'accept': 'application/json',
              'Authorization': token_bearer,
              'Content-Type': "application/json"
            }
        }
    )

    return response
}


export const getPoll = async (slug) => {
    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return response
    }

    response = await axios.get(
        `http://localhost:8000/poll/${slug}`,
        {
            headers: {
              'accept': 'application/json',
              'Authorization': token_bearer
            }
        }
    )
    return response
}


export const getAll = async () => {
    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return response
    }

    response = await axios.get(
        'http://localhost:8000/poll/all',
        {
            headers: {
              'accept': 'application/json',
              'Authorization': token_bearer
            }
        }
    )
    return response
}