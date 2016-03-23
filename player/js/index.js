// index contains
// * Root Container
// * Store initialisation
// Uses:
// * Root reducer


import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'

import rootReducer from './reducers'
import App from './components/app'


const loggerMiddleware = createLogger()

const store = createStore(
    rootReducer,
    initialState,
    applyMiddleware(
        thunkMiddleware,
        loggerMiddleware
    )
)

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('main')
)
