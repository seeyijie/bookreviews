import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom'
import { Header } from './Components'
import { Grid, Typography, Button } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

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

class Home extends Component {
    state = {

    }

    render() {
        const { classes } = this.props

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                <Typography className={classes.title} variant="subtitle1">
                    Welcome to our database!
                </Typography>
                <Typography variant="subtitle2">
                    Click on the button below to browse all books, or search by asin with the searchbar above.
                </Typography>
                <Link to="/browse" style={{ textDecoration: 'none' }}>
                    <Button className={classes.button} variant="contained">
                        Browse all books
                </Button>
                </Link>
            </Grid>
        </Fragment>
    }
}

export default withStyles(styles)(Home);
