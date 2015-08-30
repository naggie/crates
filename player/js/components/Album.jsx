var React = require("react")

var Album = React.createClass({
    // square placeholder is used for non-deterministic height -- stops many reflows on load.
    getInitialState: function() {
        return {loaded:false}
    },

    swapImg: function() {
        this.setState({loaded:true})
    },

    render: function() {
        var imgstyle = {
            display:this.state.loaded?'block':'none',
        }

        // have to show/hide via CSS instead of react re-render as react likes
        // to add spaces and mess up the document flow
        var plcstyle = {
            display:this.state.loaded?'none':'block',
            background: this.props.colour,
        }

        return (
            <div className="album pure-u-1 pure-u-sm-1-2 pure-u-md-1-4 pure-u-lg-1-6 pure-u-xl-1-8" key={this.props.id}>
                <img
                    className="pure-img-responsive"
                    onLoad={this.swapImg}
                    style={imgstyle}
                    src={'/cas/'+this.props.cover_art_ref+'.jpg'}
                />
                <img style={plcstyle} className="pure-img-responsive" src="/static/crates/placeholder.png" />

                <div className="title">{this.props.name}</div>
                <div className="artist">{this.props.artist}</div>
            </div>
        )
    },
})

module.exports = Album
