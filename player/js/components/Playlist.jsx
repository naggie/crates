var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')


var Playlist = React.createClass({
    render: function() {
        return (
            <div className="playlist content">
                <div className="pure-g masthead">
                    <div className="pure-u-1-3 cover">
                            <img className="pure-img-responsive" src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                    </div>
                    <div className="pure-u-2-3 info">
                        <h1>Fast Jungle Music</h1>
                        <p><em>Various Artists</em></p>
                        <i className="fa fa-arrow-left"></i> Back

                    </div>
                </div>
                <table className="pure-table pure-table-horizontal">
                    <thead>
                    </thead>

                    <tbody>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr className="selected">
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                        <tr>
                            <td className="cover">
                                <img src="http://farm3.staticflickr.com/2875/9069037713_1752f5daeb.jpg" />
                            </td>
                            <td>Song title</td>
                            <td>DJ Bone</td>
                            <td>What</td>
                            <td>128BPM</td>
                            <td>12B</td>
                            <td>2:33</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
})

module.exports = Playlist
