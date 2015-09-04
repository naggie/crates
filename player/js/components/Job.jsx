var React = require("react")

var Job = React.createClass({
    render: function() {
        return (
            <div className="job">
                <h2 className="content-subhead">DJ analyser</h2>
                <p>Calculate the BPM, chromakey, waveform and Chromaprint of all music</p>
                <div className="pure-g">

                    <div className="pure-u-1-5">
                        <button className="pure-button">Start now</button>
                    </div>
                    <div className="pure-u-4-5 time">
                        <p>Scheduled to run in 3 hours 7 minutes</p>
                    </div>

                    <div className="pure-u-1-5">
                        Running
                    </div>
                    <div className="pure-u-4-5 progress">
                        <div className="bar"></div>
                    </div>
                </div>
            </div>
        )
    },
})

module.exports = Job
