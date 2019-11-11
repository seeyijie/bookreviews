import React, { Component, Fragment } from 'react';
import { Header, BrowseAllEntries } from './Components'
import { Grid, Typography } from '@material-ui/core';
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
            searchBooksmetadata: []
        }
    }

    // loadNewSearch() {
    //     if (this.state.inPage === true && this.props.location.state.isSearch === true) {
    //         const searchstring = this.props.location.state.searchstring
    //         const url = `http://127.0.0.1:5000/api/titlematching/${searchstring}`
    //         axios.get(url)
    //             .then(response => {
    //                 this.setState({
    //                     isLoading: false,
    //                     reloadPage: true,
    //                     booksmetadata: response.data,
    //                     inPage: false
    //                 })
    //             })
    //     }
    //     else {
    //         // this.state.inPage = true;
    //         this.setState({
    //             inPage: true,
    //             reloadPage: false
    //         })
    //         return null
    //     }
    // }

    // shouldComponentUpdate() {
    //     if (this.state.reloadPage === true) {
    //         return true
    //     }
    //     else {
    //         return false
    //     }
    // }

    render() {
        const { classes } = this.props
        const { booksmetadata } = this.state;
        const loadingMessage = <Typography className={classes.loadtext}>Loading... Please wait</Typography>

        // this.loadNewSearch();

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                {this.state.isLoading ? loadingMessage : <BrowseAllEntries booksmetadata={booksmetadata} />}
            </Grid>
        </Fragment>
    }

    componentDidMount() {
        const searchstring = this.props.location.state.searchstring
        const url = `http://127.0.0.1:5000/api/titlematching/${searchstring}`
        axios.get(url)
            .then(response => {
                this.setState({
                    isLoading: false,
                    booksmetadata: response.data,
                    inPage: false
                })
            })
    }
}

export default withStyles(styles)(SearchResults);
