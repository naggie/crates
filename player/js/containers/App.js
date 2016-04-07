import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'

import AlbumBrowser from '../components/AlbumBrowser.jsx'

import {browse_all,filter_by_text,filter_by_letter,load_page} from '../actions/browserActions'


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
      filter_by_letter: letter => dispatch(filter_by_letter(letter)),
  }
}

export default connect(
        mapStateToProps,
        mapDispatchToProps
)(AlbumBrowser)
