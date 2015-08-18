var React = require("react")

var SearchBox = React.createClass({
    componentDidMount: function() {
        this.refs.search.getDOMNode.focus()
    },
    render: function() {
        return
            <form>
                <input ref="search" type="text" placeholder="Search..."/>
            </form>

    },
})

module.exports = SearchBox
