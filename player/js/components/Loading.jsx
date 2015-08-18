var React = require("react")

class Loading extends React.Component {
    render() {
        return (
            <div className="loading pure-u-1">
                <i className="fa fa-spin fa-3x fa-circle-o-notch" />
            </div>
        )
    }
}

exports = Loading
