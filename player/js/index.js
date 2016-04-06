import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'

//import rootReducer from './reducers/rootReducer'
import rootReducer from './reducers/browserReducer'

import App from './containers/App'


const loggerMiddleware = createLogger()

const store = createStore(
    rootReducer,
    {},
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
