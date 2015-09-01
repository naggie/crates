var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

var Player = React.createClass({
    render: function() {
        return (
            <div className="player pure-g">
                <div className="pure-u-lg-3-24 buttons">
                    <i className="fa fa-backward"></i>
                    <i className="fa fa-play"></i>
                    <i className="fa fa-forward"></i>
                </div>
                <div className="pure-u-lg-1-24 time">1:20</div>
                <div className="pure-u-lg-11-24">
                    <div className="progress">
                        <div className="bar"></div>
                        <div className="cursor">
                            <i className="fa fa-circle"></i>
                        </div>
                    </div>
                </div>
                <div className="pure-u-lg-1-24 time">5:24</div>
                <div className="pure-u-lg-1-24 buttons">
                    <i className="fa fa-heart-o"></i>
                </div>
                <div className="pure-u-lg-2-24 cover">
                    <img className="pure-img-responsive" src="http://localhost:8000/cas/7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f.jpg" />
                </div>
                <div className="pure-u-lg-5-24 info">
                    <div className="title">Fast Jungle Music</div>
                    <div className="artist">Various Artists</div>
                </div>
            </div>
        )
    }
})

module.exports = Player
