import React from 'react';
import { Grid, List, ListItem } from '@material-ui/core';
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
}));

function BookInfo({ bookID, categories, description, imUrl, price, also_viewed, buy_after_viewing, sales_rank, title }) {
    const classes = useStyles();

    return <Grid className={classes.bigGrid} container direction='row'>
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
                <ListItem>Also Viewed: {also_viewed.map((book) => book + " ")}</ListItem>
                <ListItem>Also Bought: {buy_after_viewing.map((book) => book + " ")}</ListItem>
            </List>
        </Grid>
    </Grid>
}

export default BookInfo;