import { createStore, applyMiddleware } from 'redux'
import { routerMiddleware, push } from 'react-router-redux'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'
import { Router, Route, Link, hashHistory , Redirect} from 'react-router'

// containers
import AlbumBrowser from './containers/AlbumBrowser.jsx'
import AlbumView from './containers/AlbumView.jsx'
import Player from './containers/Player.jsx'

import {browse_all,filter_by_text,filter_by_letter,load_page} from './actions/browserActions'

//import rootReducer from './reducers/rootReducer'
import rootReducer from './reducers/browserReducer'


const loggerMiddleware = createLogger()

const store = createStore(
    rootReducer,
    {},
    applyMiddleware(
        thunkMiddleware,
        loggerMiddleware,
        routerMiddleware(hashHistory),
    )
)

const history = syncHistoryWithStore(hashHistory,store)


render(
    <Provider store={store}>
        <Router history={history}>
            <Redirect from="/" to="/albums" />
            <Route path="/albums/letters/:letter" component={AlbumBrowser} />
            <Route path="/albums/:id" component={AlbumView} />
            <Route path="/albums" component={AlbumBrowser} />
        </Router>
    </Provider>,
    document.getElementById('main')
)
