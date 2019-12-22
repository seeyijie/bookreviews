import React, { Component, Fragment } from 'react';
import { Header, BrowseAllEntries } from './Components'
import { Grid, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';
import * as config from './Data/config';
import Box from "@material-ui/core/Box";

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

class SearchResults extends Component {
    constructor(props) {
        super(props)

        this.state = {
            isLoading: true,
            booksmetadata: [],
            inPage: false,
            reloadPage: false,
            searchBooksmetadata: [],
            hasResults: true
        }
    }

    render() {
        // console.log("Rendered")
        const { classes } = this.props;
        const { booksmetadata, hasResults } = this.state;
        const loadingMessage = <Typography className={classes.loadtext}>Loading... Please wait</Typography>

        // this.loadNewSearch();
        // console.log(this.props.location.state.searchstring);
        if (this.state.inPage === true && this.props.location.state.searchstring != null) {
            this.componentDidMount();
        }

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                <Box p={2} bgcolor="background.paper" />
                <Typography noWrap>
                    {this.state.hasResults ? null : "No search results found"}
                </Typography>
                {this.state.isLoading ? loadingMessage : <BrowseAllEntries booksmetadata={booksmetadata} />}
            </Grid>
        </Fragment>
    }

    componentDidMount() {
        // console.log("ComponentDidMount")
        const searchstring = this.props.location.state.searchstring
        // const url = `http://127.0.0.1:5000/api/titlematching/${searchstring}`
        const url =`${config.flaskip}/api/titlematching/${searchstring}`
        axios.get(url)
            .then(response => {
                this.props.location.state.searchstring = null;
                if (response.data.length === 0) {
                    this.setState({
                        isLoading: false,
                        booksmetadata: response.data,
                        inPage: true,
                        hasResults: false
                    });
                } else {
                    this.setState({
                        isLoading: false,
                        booksmetadata: response.data,
                        inPage: true,
                        hasResults: true
                    });
                }
            })
    }
}

export default withStyles(styles)(SearchResults);
