var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

// TODO placeholders for responseive images

var Playlist = React.createClass({
    getInitialState: function() {
        return {
            items : [
                {
                    title:'Whatbruv mix',
                    artist:'DJ BONE',
                    cover_art_ref: '7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f',
                    bpm:'189BPM',
                    key:'9A',
                    length:'3:22',
                    bitrate:'320kbps',
                },
                {
                    title:'Whatbruv mix',
                    artist:'DJ BONE',
                    cover_art_ref: '7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f',
                    bpm:'189BPM',
                    key:'9A',
                    length:'3:22',
                    bitrate:'320kbps',
                },
                {
                    title:'Whatbruv mix',
                    artist:'DJ BONE',
                    cover_art_ref: '7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f',
                    bpm:'189BPM',
                    key:'9A',
                    length:'3:22',
                    bitrate:'320kbps',
                },
                {
                    title:'Whatbruv mix',
                    artist:'DJ BONE',
                    cover_art_ref: '7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f',
                    bpm:'189BPM',
                    key:'9A',
                    length:'3:22',
                    bitrate:'320kbps',
                },
                {
                    title:'Whatbruv mix',
                    artist:'DJ BONE',
                    cover_art_ref: '7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f',
                    bpm:'189BPM',
                    key:'9A',
                    length:'3:22',
                    bitrate:'320kbps',
                },
            ],
            selected : 3,
        }
    },
    render: function() {
        return (
            <div className="playlist content">
                <div className="pure-g masthead">
                    <div className="pure-u-1-3 cover">
                        <img className="pure-img-responsive" src={'/cas/'+this.props.cover_art_ref+'.jpg'} />
                    </div>
                    <div className="pure-u-2-3 info">
                        <h1>{this.props.name}</h1>
                        <p><em>{this.props.artist}</em></p>
                        <p><i className="fa fa-arrow-left"></i> Back</p>
                    </div>
                </div>
                <table className="pure-table pure-table-horizontal">
                {
                    this.state.items.map((props,i) => {
                        return <tr className={i == this.state.selected?'selected':''}>
                            <td className="cover">
                                <img src={'/cas/'+props.cover_art_ref+'.jpg'} />
                            </td>
                            <td>{props.title}</td>
                            <td>{props.artist}</td>
                            <td>{props.bpm}</td>
                            <td>{props.key}</td>
                            <td>{props.length}</td>
                            <td>{props.bitrate}</td>
                        </tr>
                    })
                }
                </table>
            </div>
        )
    }
})

module.exports = Playlist
