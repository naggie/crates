var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

var Player = React.createClass({
    getInitialState: function() {
        this.audio = document.createElement('audio')

        // TODO support M4A as well as MP3
        this.audio.src = '/cas/'+this.props._ref+'.mp3'
        this.audio.load()

        return {
            elapsed: '0:00',
            elapsed_percent: 30,
            total:'9:99',
        }
    },
    render: function() {
        return (
            <div className="player pure-g">
                <div className="pure-u-lg-3-24 buttons">
                    <i className="fa fa-backward"></i>
                    <i className="fa fa-play" onClick={this.audio.play.bind(this.audio)}></i>
                    <i className="fa fa-forward"></i>
                </div>
                <div className="pure-u-lg-1-24 time">{this.state.elapsed}</div>
                <div className="pure-u-lg-11-24">
                    <div className="progress">
                        <div className="bar" style={{
                            width:this.state.elapsed_percent+'%',
                            backgroundColor:this.props.colour,
                        }}></div>
                        <div className="cursor" style={{left:this.state.elapsed_percent+'%'}}>
                            <i className="fa fa-circle"></i>
                        </div>
                    </div>
                </div>
                <div className="pure-u-lg-1-24 time">{this.state.total}</div>
                <div className="pure-u-lg-1-24 buttons">
                    <i className="fa fa-heart-o"></i>
                </div>
                <div className="pure-u-lg-2-24 cover">
                    <img className="pure-img-responsive" src={'/cas/'+this.props.cover_art_ref+'.jpg'} />
                </div>
                <div className="pure-u-lg-5-24 info">
                    <div className="title">{this.props.title}</div>
                    <div className="album">{this.props.album}</div>
                    <div className="artist">{this.props.album_artist}</div>
                </div>
            </div>
        )
    }
})

module.exports = Player
