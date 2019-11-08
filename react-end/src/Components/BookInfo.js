import React from 'react';
import { Link } from 'react-router-dom'
import { Grid, List, ListItem, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    bigGrid: {
        paddingLeft: theme.spacing(2),
        paddingRight: theme.spacing(2)
    },
    smallGrid: {
        paddingLeft: theme.spacing(2),
        paddingTop: theme.spacing(2)
    },
    button: {
        marginTop: '20px',
        border: 0,
        borderRadius: 5,
    }
}));

function BookInfo({ bookID, categories, description, imUrl, price, also_viewed, buy_after_viewing, sales_rank, title }) {
    const classes = useStyles();

    return <Grid className={classes.bigGrid} container direction='column'>

        <Link to="/browse" style={{ textDecoration: 'none' }}>
            <Button className={classes.button} variant="contained">
                Return to browse all books
                </Button>
        </Link>
        <Grid className={classes.bigGrid} container direction='row'>
            <Grid className={classes.smallGrid} item md>
                <img src={imUrl} style={{ height: 220 }} alt="cannot be loaded" />
            </Grid>
            <Grid className={classes.smallGrid} item md="10">
                <List>
                    <ListItem>Asin: {bookID}</ListItem>
                    <ListItem>Title: {title}</ListItem>
                    <ListItem>Categories: {categories}</ListItem>
                    <ListItem>Sales Rank: {sales_rank}</ListItem>
                    <ListItem>Description: {description}</ListItem>
                    <ListItem>Price: {price}</ListItem>
                    {also_viewed ? <ListItem>Also Viewed: {also_viewed.map((book) => book + " ")}</ListItem> : <ListItem>Also Viewed: </ListItem>}
                    {buy_after_viewing ? <ListItem>Also Bought: {buy_after_viewing.map((book) => book + " ")}</ListItem> : <ListItem>Also Bought: </ListItem>}
                </List>
            </Grid>
        </Grid>
    </Grid>
}

export default BookInfo;