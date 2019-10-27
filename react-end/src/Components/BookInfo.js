import React from 'react';
import { Grid, List, ListItem } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { booksmetadata } from '../Data/hardmongo';

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

function BookInfo({ bookID }) {
    const classes = useStyles();

    return <Grid>
        helloergfd
    </Grid>
}

export default BookInfo;