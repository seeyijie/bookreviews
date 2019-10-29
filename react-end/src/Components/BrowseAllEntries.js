import React from 'react';
import { Link } from 'react-router-dom'
import { Grid, List, ListItem } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    bigGrid: {
        paddingLeft: theme.spacing(2),
        paddingRight: theme.spacing(2)
    },
    leftGrid: {
        paddingLeft: theme.spacing(2),
        paddingTop: theme.spacing(2)
    },
    rightGrid: {
        paddingLeft: theme.spacing(2),
        paddingTop: theme.spacing(2)
    },
    picture: {
        paddingLeft: theme.spacing(30)
    }
}));

function BrowseAllEntries({ booksmetadata }) {
    const classes = useStyles();

    const booksArray = booksmetadata.map((book) =>
        <Grid className={classes.bigGrid} container direction='row'>
            <Grid className={classes.leftGrid} item md>
                <Link className={classes.picture} to={"/books/" + book.asin} style={{ textDecoration: 'none' }}>
                    <img src={book.imUrl} style={{ height: 220, width: 220 }} alt="cannot be loaded" />
                </Link>
            </Grid>
            <Grid className={classes.rightGrid} item md key={book.asin}>
                <List>
                    <ListItem>Asin: {book.asin}</ListItem>
                    <ListItem>Title: {book.title}</ListItem>
                    <ListItem>Price: {book.price}</ListItem>
                    {/* <ListItem>Also Bought: {book.related.also_bought.map((book) => book + " ")}</ListItem> */}
                    {/* <ListItem>Also Viewed: {book.related.also_viewed.map((book) => book + " ")}</ListItem> */}
                    {/* <ListItem>Bought Together: {book.bought_together.map((book) => book + " ")}</ListItem> */}
                </List>
            </Grid>
        </Grid>
    )

    return <Grid>
        {booksArray}
    </Grid>
}

export default BrowseAllEntries;