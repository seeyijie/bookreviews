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

function BrowseAllEntries({ booksmetadata }) {
    const classes = useStyles();

    const booksArray = booksmetadata.map((book) =>
        <Grid className={classes.bigGrid} container direction='row'>
            <Grid className={classes.smallGrid} item md>
                <img src={book.imUrl} style={{ height: 220 }} alt="cannot be loaded" />
            </Grid>
            <Grid className={classes.smallGrid} item md="10" key={book.asin}>
                <List>
                    <ListItem>Asin: {book.asin}</ListItem>
                    <ListItem>Title: {book.title}</ListItem>
                    <ListItem>Price: {book.price}</ListItem>
                    <ListItem>Also Bought: {book.related.also_bought.map((book) => book + " " )}</ListItem>
                    <ListItem>Also Viewed: {book.related.also_viewed.map((book) => book + " " )}</ListItem>
                    <ListItem>Bought Together: {book.bought_together.map((book) => book + " " )}</ListItem>
                </List>
            </Grid>
        </Grid>
    )

    return <Grid>
        {booksArray}
    </Grid>
}

export default BrowseAllEntries;