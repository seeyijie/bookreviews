import React, { Component, Fragment } from 'react';
import { Header, BrowseAllEntries } from './Components'
import { withStyles } from '@material-ui/core/styles';
import { booksmetadata } from './Data/hardmongo';

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

class Browse extends Component {
    state = {
    }

    render() {
        return <Fragment>
            <Header />
            <BrowseAllEntries
                booksmetadata={booksmetadata}
            />
        </Fragment>
    }
}

export default withStyles(styles)(Browse);
