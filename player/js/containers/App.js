import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'

import AlbumBrowser from '../components/AlbumBrowser'

import {browse_all,filter_by_text,filter_by_letter,load_page} from '../actions/browserActions'


function mapStateToProps(state) {
  return {
  }
}

function mapDispatchToProps(state) {
  return {
  }
}

export default connect(
        mapStateToProps,
        mapDispatchToProps
)(AlbumBrowser)
