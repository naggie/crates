var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

class AZ extends React.Component {
    // TODO use purecss.io primitives for this
    constructor(props) {
        this.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')
    }

    updateChar(char) {
        this.props.onCharChange(char)
    }

    render() {
        return (
            <div className="pure-menu alphabet">
                 <ul className="pure-menu-list">
                    {
                        this.alphabet.map((char,i) => {
                            var classes = classNames('pure-menu-item',{
                                'pure-menu-selected' : char == this.props.selected,
                            })
                            return <li
                                className={classes}
                                key={i}
                                onClick={this.updateChar.bind(this,char)}>
                                <a href="#" className="pure-menu-link">{char}</a>
                            </li>
                        })
                    }
                </ul>
            </div>
        )
    }

}

exports = AZ
