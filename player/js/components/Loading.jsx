var React = require("react")

var Loading = React.createClass({
    render: function() {
        return (
            <div className="loading pure-u-1">
                <i className="fa fa-spin fa-3x fa-circle-o-notch" />
            </div>
        )
    },
})

module.exports = Loading
