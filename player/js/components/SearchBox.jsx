var React = require("react")


class SearchBox extends React.Component {
    componentDidMount() {
        this.refs.search.getDOMNode.focus()
    }
    render() {
        return
            <form>
                <input ref="search" type="text" placeholder="Search..."/>
            </form>

    }
}

exports = SearchBox
