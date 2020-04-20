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


// TASKS

export const createTask = async (rawMessage, slug) => {
    if (!rawMessage) {
        return { status: "error", message: "Please provide task description!" }
    }
    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return { status: "error", message: "Not Authenticated" }
    }

    const task = { description: rawMessage }
    const payload = {
        task,
        slug
    }

    try {
        response = await axios.post(
            'http://localhost:8000/poll/create-task',
            JSON.stringify(payload),
            {
                headers: {
                  'accept': 'application/json',
                  'Authorization': token_bearer,
                  'Content-Type': "application/json"
                }
            }
        )
    } catch(e) {
        console.log('e', e.response);
        return { status: "error", message: e.response.data.detail }
    }

    return response.data
}


export const allowVotes = async (rawMessage, slug, task) => {
    task.allow_votes = true
    console.log('ALLOW task', task);
    const response = await updateTask(rawMessage, slug, task)
    return response
}


export const disallowVotes = async (rawMessage, slug, task) => {
    task.allow_votes = false
    const response = await updateTask(rawMessage, slug, task)
    return response
}


export const updateTask = async (rawMessage, slug, task) => {
    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return { status: "error", message: "Not Authenticated" }
    }

    const payload = {
        task,
        slug
    }

    try {
        response = await axios.post(
            'http://localhost:8000/poll/update-task',
            JSON.stringify(payload),
            {
                headers: {
                  'accept': 'application/json',
                  'Authorization': token_bearer,
                  'Content-Type': "application/json"
                }
            }
        )
    } catch(e) {
        console.log('e', e.response);
        return { status: "error", message: e.response.data.detail }
    }

    return response.data

}


export const closeTask = async (rawMessage, slug, task) => {
    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return { status: "error", message: "Not Authenticated" }
    }

    const payload = {
        slug
    }

    try {
        response = await axios.post(
            'http://localhost:8000/poll/close-task',
            JSON.stringify(payload),
            {
                headers: {
                  'accept': 'application/json',
                  'Authorization': token_bearer,
                  'Content-Type': "application/json"
                }
            }
        )
    } catch(e) {
        console.log('e', e.response);
        return { status: "error", message: e.response.data.detail }
    }

    return response.data
}


export const vote = async (rawMessage, slug, task) => {
    const ALLOWED_VOTES = ["0", "1/2", "1", "2", "3", "5", "8", "13"]
    const vote = rawMessage.replace(/\s/g, "")

    if (!ALLOWED_VOTES.includes(vote)) {
        return {
            status: "error",
            message: "Please provide a valid vote from the list: 0; 1/2; 1; 2; 3; 5; 8; 13"
        }
    }

    const token_bearer = localStorage.getItem("auth")
    let response = null

    if (!token_bearer) {
        return { status: "error", message: "Not Authenticated" }
    }

    const payload = {
        slug,
        vote: rawMessage
    }

    try {
        response = await axios.post(
            'http://localhost:8000/poll/vote',
            JSON.stringify(payload),
            {
                headers: {
                  'accept': 'application/json',
                  'Authorization': token_bearer,
                  'Content-Type': "application/json"
                }
            }
        )
    } catch(e) {
        console.log('e', e.response);
        return { status: "error", message: e.response.data.detail }
    }

    console.log('ON CRUD response', response);

    return response.data
}











