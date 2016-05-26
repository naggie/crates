var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

// TODO placeholders for responsive images

const AlbumView = ({items, cover_art_ref, name, artist, cursor}) => (
    <div className="playlist content">
        <div className="pure-g masthead">
            <div className="pure-u-1-3 cover">
                <img className="pure-img-responsive" src={'/cas/'+cover_art_ref+'.jpg'} />
            </div>
            <div className="pure-u-2-3 info">
                <h1>{name}</h1>
                <p><em>{artist}</em></p>
                <p><i className="fa fa-arrow-left"></i> Back</p>
            </div>
        </div>
        <table className="pure-table pure-table-horizontal">
        {
            items.map((item,i) => {
                return <tr
                        key={i}
                        className={i==cursor?'selected':''}
                        onClick={this.props.selectItem.bind(this,item)}
                    >
                    <td className="cover">
                        <img src={'/cas/'+item.cover_art_ref+'.jpg'} />
                    </td>
                    <td>{item.title}</td>
                    <td>{item.artist}</td>
                    <td>{item.bpm}</td>
                    <td>{item.key}</td>
                    <td>{item.length}</td>
                    <td>{item.bitrate}</td>
                </tr>
            })
        }
        </table>
    </div>
)

export default AlbumView
