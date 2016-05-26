import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'

import { Router, Route, Link, hashHistory , Redirect} from 'react-router'

// containers
import AlbumBrowser from './AlbumBrowser.jsx'
import AlbumView from './AlbumView.jsx'
import Player from './Player.jsx'

import {browse_all,filter_by_text,filter_by_letter,load_page} from '../actions/browserActions'

const Browser = () => {
    return <Router history={hashHistory}>
        <Redirect from="/" to="/albums" />
        <Route path="/albums/letter/:letter" component={AlbumBrowser} />
        <Route path="/albums/:id" component={AlbumView} />
        <Route path="/albums" component={AlbumBrowser} />
    </Router>

}

export default Browser
