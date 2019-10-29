import React, { Component, Fragment } from 'react';
import { Header, BrowseAllEntries } from './Components'
import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';
// import { booksmetadata } from './Data/hardmongo';

const styles = () => ({
    title: {
        marginTop: '50px'
    },
    button: {
        marginTop: '50px',
        border: 0,
        borderRadius: 5,
    }
});

class Browse extends Component {
    constructor(props) {
        super(props)

        this.state = {
            isLoading: true,
            booksmetadata: []
        }
    }

    componentDidMount() {
        // call flask api
        const url = `http://127.0.0.1:5000/api/allbooks`
        axios.get(url)
            .then(response => {
                this.setState({
                    isLoading: false,
                    booksmetadata: response.data
                })
            })
    }

    render() {
        const { booksmetadata } = this.state;
        const loadingMessage = <Typography>Loading... Please wait</Typography>

        return <Fragment>
            <Header />
            {this.state.isLoading ? loadingMessage : <BrowseAllEntries booksmetadata={booksmetadata} />}
        </Fragment>
    }
}

export default withStyles(styles)(Browse);
