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

function BookInfo({ bookID, categories, description, imUrl, price, also_bought, also_viewed, buy_after_viewing, sales_rank, title }) {
    const classes = useStyles();

    console.log(also_bought)
    console.log(also_viewed)
    console.log(buy_after_viewing)
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
            <Grid className={classes.smallGrid} item md={10}>
                <List>
                    <ListItem>Asin: {bookID}</ListItem>
                    <ListItem>Title: {title}</ListItem>
                    <ListItem>Categories: {categories}</ListItem>
                    <ListItem>Sales Rank: {sales_rank}</ListItem>
                    <ListItem>Description: {description}</ListItem>
                    <ListItem>Price: {price}</ListItem>
                    <ListItem>Also Bought: {also_bought && also_bought.length > 0 ? also_bought.map((book) => book + " ") : null} </ListItem>
                    <ListItem>Also Viewed: {also_viewed && also_viewed.length > 0 ? also_viewed.map((book) => book + " ") : null} </ListItem>
                    <ListItem>Bought After Viewing: {buy_after_viewing && buy_after_viewing.length > 0 ? buy_after_viewing.map((book) => book + " ") : null} </ListItem>
                </List>
            </Grid>
        </Grid>
    </Grid>
}

export default BookInfo;