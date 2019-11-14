import React, { Component, Fragment } from 'react';
import { Header } from './Components'
import { Logtable } from './Components'
import { Grid, Typography, Button } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';

const styles = () => ({
    title: {
        marginTop: '50px'
    },
    button: {
        marginTop: '50px',
        border: 0,
        borderRadius: 5,
    },
    loadtext: {
        marginTop: '50px',
    }
});

class Log extends Component {
    constructor(props) {
        super(props)

        this.state = {
            isLoading: true,
            log_json: null
        }
    }

    componentDidMount() {
        // call flask api to get all logs and store into log_json
        const url = `http://127.0.0.1:5000/getlog`
        axios.get(url)
            .then(response => response.data)
            .then(log => {
                this.setState({
                    isLoading: false,
                    log_json: log
                })
            })
    }

    onClickHandler(e) {
        // call flask api to delete all logs
        const url = `http://127.0.0.1:5000/deletelogs`
        axios.get(url)
        this.setState({
            isLoading: true,
            log_json: null
        })
        this.componentDidMount()
    }

    render() {
        const { classes } = this.props
        const { isLoading, log_json } = this.state
        const loadingMessage = <Typography className={classes.loadtext}>Retrieving logs... Please wait</Typography>

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                {/* <Button className={classes.button} variant="contained" onClick={this.onClickHandler.bind(this)}>Delete all logs</Button> */}
                {isLoading ? loadingMessage : <Logtable log_json={log_json} />}
            </Grid>
        </Fragment>
    }
}

export default withStyles(styles)(Log);
