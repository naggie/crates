import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'

import { Router, Route, Link, hashHistory , Redirect} from 'react-router'

import AlbumBrowser from '../components/AlbumBrowser.jsx'
import AlbumView from '../components/AlbumView.jsx'
import Player from '../components/Player.jsx'

import {browse_all,filter_by_text,filter_by_letter,load_page} from '../actions/albumBrowser'

const Browser = ({playlist,}) => {

    var out = []


    if (playlist.items.length)
        out.push(
            <Player
                cover_art_ref="7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f"
                title="Jungle music (original)"
                album="Fast Jungle Music"
                album_artist="Hospital records"
                _ref="6c1efd7cbc14ab9a8444bd62caeb878cd3879c5dac8eec3fa0aab7e358a97d0b"
                colour="#b3bf9c"
            />
        )


    return out

}

function mapStateToProps(state) {
  return {
      albums: state.browser.items,
      loading: state.browser.loading,
      exhausted: state.browser.exhausted,
      letter: state.browser.letter,
  }
}

function mapDispatchToProps(dispatch) {
  return {
      onLoad: () => dispatch(browse_all()),
      onNewPageRequest: () => dispatch(load_page()),
      onSelect: id => console.log(id),
      //onSelect: () => dispatch(browse_all()),
      filter_by_letter: letter => dispatch(filter_by_letter(letter)),
  }
}

export default connect(
        mapStateToProps,
        mapDispatchToProps
)(Browser)
