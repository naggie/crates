var React = require("react")

class Album extends React.Component {
    // square placeholder is used for non-deterministic height -- stops many reflows on load.
    constructor() {
        this.state = {'loaded':false}
        // automate this: http://www.newmediacampaigns.com/blog/refactoring-react-components-to-es6-classes
        this.swapImg = this.swapImg.bind(this) // TODO this elsewhere instead of passing parent this
    }

    swapImg() {
        this.setState({loaded:true})
    }

    render() {
        var imgstyle = {display:this.state.loaded?'block':'none'}
        var plcstyle = {display:this.state.loaded?'none':'block'}

        return (
            <div className="album pure-u-1 pure-u-md-1-3 pure-u-lg-1-6 pure-u-xl-1-7" key={this.props.id}>
                <img
                    className="pure-img-responsive"
                    onLoad={this.swapImg}
                    style={imgstyle}
                    src={'/cas/'+this.props.cover_art_ref}
                />
                <img style={plcstyle} className="pure-img-responsive" src="/static/crates/placeholder.png" />

                <div className="title">{this.props.name}</div>
                <div className="artist">{this.props.artist}</div>
            </div>
        )
    }
}

exports = Album
