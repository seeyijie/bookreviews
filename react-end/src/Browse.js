import React, { Component, Fragment } from 'react';
import { Header, BrowseAllEntries } from './Components';
import { Grid, Typography, Button } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';
import * as config from './Data/config';

const styles = () => ({
    title: {
        marginTop: '50px'
    },
    button: {
        marginTop: '10px',
        border: 0,
        borderRadius: 5,
    },
    loadtext: {
        marginTop: '50px',
        marginBottom: '20px'
    },
    leftGrid: {
        paddingLeft: '50px',
        paddingTop: '50px'
    },
    rightGrid: {
        paddingLeft: '50px',
        paddingTop: '50px'
    },
});

class Browse extends Component {
    constructor(props) {
        super(props)

        this.state = {
            isLoading: true,
            booksmetadata: [],
            isSearch: false,
            searchBooksmetadata: [],
            pageNum: 1,
        }

        this.previousPage = this.previousPage.bind(this);
        this.nextPage = this.nextPage.bind(this);
    }

    async previousPage() {
        await this.setState(prevState => {
            if (prevState.pageNum === 1) {
                return { isLoading: true }
            }
            else {
                return {
                    pageNum: prevState.pageNum - 1,
                    isLoading: true
                }
            }
        })
        this.componentDidMount();
    }

    async nextPage() {
        await this.setState(prevState => {
            return {
                pageNum: prevState.pageNum + 1,
                isLoading: true
            }
        })
        this.componentDidMount();
    }

    componentDidMount() {
        const url = `${config.flaskip}/api/allbooks/${this.state.pageNum}`

        axios.get(url)
            .then(response => {
                this.setState({
                    isLoading: false,
                    booksmetadata: response.data
                })
            })
    }

    render() {
        const { classes } = this.props
        const { booksmetadata } = this.state;
        const loadingMessage = <Typography className={classes.loadtext}>Loading... Please wait</Typography>

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                {this.state.isLoading ? loadingMessage : <BrowseAllEntries booksmetadata={booksmetadata} />}
            </Grid>
            <Grid container alignItems='center' direction='column'>
                <Typography variant="subtitle2">
                    Page {this.state.pageNum}
                </Typography>
            </Grid>
            <Grid className={classes.bigGrid} container direction='row'>
                <Grid container alignItems='center' direction='column' item md>
                    <Button onClick={this.previousPage} className={classes.button} variant="contained">
                        Previous page
                </Button>
                </Grid>
                <Grid container alignItems='center' direction='column' item md>
                    <Button onClick={this.nextPage} className={classes.button} variant="contained">
                        Next page
                </Button>
                </Grid>
            </Grid>
        </Fragment >
    }
}

export default withStyles(styles)(Browse);
