var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

// TODO preload next track
// TODO KB shortcuts
// TODO mark along the progress bar what parts the client has buffered. Wow!
// TODO support video. Should be possible to simply swap the element.
function seconds_to_clock(elapsed_seconds) {
    if (!elapsed_seconds || typeof elapsed_seconds !='number') return ''

    var hours = parseInt(elapsed_seconds/3600)
    var minutes = parseInt(elapsed_seconds/60)
    var seconds = parseInt(elapsed_seconds%60)

    // hooray for dynamic typing
    if (seconds < 10)
        seconds = `0${seconds}`

    if (hours)
        return `${hours}:${minutes}:${seconds}`
    else
        return `${minutes}:${seconds}`
}

var Player = React.createClass({
    getInitialState: function() {
        return {
            audio_state:'LOADING',
            elapsed_seconds:0,
            total_seconds:0,
        }
    },

    initAudio: function() {

        // TODO put this in changed props handler also by a separate method
        this.audio = document.createElement('audio')
        this.audio.autoplay = true

        // TODO support M4A as well as MP3
        this.audio.src = '/cas/'+this.props._ref+'.mp3'
        this.audio.load()

        // TODO timeranges for buffering (extra progress bar) (buffer property, progress event)
        this.audio.addEventListener('canplaythrough',() => this.setState({audio_state:this.audio.autoplay?'PLAYING':'READY'}) )
        this.audio.addEventListener('ended',() => this.setState({audio_state:'STOPPED'}) )
        this.audio.addEventListener('pause',() => this.setState({audio_state:'PAUSED'}) )
        this.audio.addEventListener('playing',() => this.setState({audio_state:'PLAYING'}) )
        this.audio.addEventListener('seeking',() => this.setState({audio_state:'LOADING'}) )

        this.audio.addEventListener('timeupdate',this.update_time)
    },
    update_time: function() {
        this.setState({
            elapsed_seconds: this.audio.currentTime,
            total_seconds: this.audio.duration,
        })
    },

    removeAudio: function() {
        delete this.audio
    },

    componentWillMount : function(){ this.initAudio()},
    componentWillReceiveProps : function(){ this.initAudio()},
    componentWillUnmount : function(){ this.removeAudio()},

    seek: function(event) {
        var node = React.findDOMNode(this.refs.progress)
        var left = node.getBoundingClientRect().left
        var width = node.offsetWidth
        var offset = event.clientX - left

        if (this.audio.seekable.length)
            this.audio.currentTime = offset*this.state.total_seconds/width
    },

    playpause: function() {
        switch (this.state.audio_state) {
            case 'PLAYING':
                this.audio.pause()
            break
            case 'STOPPED':
                this.audio.currentTime = 0
            case 'PAUSED':
                this.audio.play()
            break
        }
    },
    render: function() {
        var elapsed_time = seconds_to_clock(this.state.elapsed_seconds)
        var total_time = seconds_to_clock(this.state.total_seconds)
        var elapsed_percent = 100*this.state.elapsed_seconds/this.state.total_seconds

        var playicon
        switch (this.state.audio_state) {
            case 'LOADING':
                playicon = 'fa fa-fw fa-circle-o-notch fa-spin'
            break
            case 'PLAYING':
                playicon = 'fa fa-fw fa-pause'
            break
            case 'PAUSED':
            case 'STOPPED':
                playicon = 'fa fa-fw fa-play'
            break
        }

        return (
            <div className="player pure-g">
                <div className="pure-u-lg-3-24 buttons">
                    <i className="fa fa-backward disabled"></i>
                    <i className={playicon} onClick={this.playpause} c></i>
                    <i className="fa fa-forward disabled"></i>
                </div>
                <div className="pure-u-lg-1-24 time">{elapsed_time}</div>
                <div className="pure-u-lg-11-24">
                    <div className="progress" ref="progress" onMouseUp={this.seek}>
                        <div className="bar" style={{
                            width:elapsed_percent+'%',
                            backgroundColor:this.props.colour,
                        }}></div>
                        <div className="cursor" style={{left:elapsed_percent+'%'}}>
                            <i className="fa fa-circle"></i>
                        </div>
                    </div>
                </div>
                <div className="pure-u-lg-1-24 time">{total_time}</div>
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
