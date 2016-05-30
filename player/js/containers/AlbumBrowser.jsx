import { connect } from 'react-redux'
import AlbumBrowser from '../components/AlbumBrowser.jsx'

import {browse_all,filter_by_text,filter_by_letter,load_page} from '../actions/browserActions'


function mapStateToProps(state,ownProps) {
  return {
      albums: state.browser.items,
      loading: state.browser.loading,
      exhausted: state.browser.exhausted,
      letter: ownProps.params.letter,
  }
}

function mapDispatchToProps(dispatch) {
  return {
      //onReady: () => dispatch(browse_all()),
      onReady: letter => dispatch(filter_by_letter(letter)),
      filter_by_letter: letter => dispatch(filter_by_letter(letter)),
      onNewPageRequest: () => dispatch(load_page()),
      onSelect: id => console.log(id),
      letter: letter => dispatch(filter_by_letter(letter)),
  }
}

export default connect(
        mapStateToProps,
        mapDispatchToProps
)(AlbumBrowser)
