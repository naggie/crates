var React = require("react")
var classNames = require('classnames')
var utils = require('../utils')

var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')

var AZ = React.createClass({
    updateChar: function(char) {
        this.props.onCharChange(char)
    },
    render: function() {
        return (
            <div className="pure-menu alphabet">
                 <ul className="pure-menu-list">
                    {
                        alphabet.map((char,i) => {
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
})

module.exports = AZ
