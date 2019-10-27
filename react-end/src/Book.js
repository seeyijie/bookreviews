import React, { Component, Fragment } from 'react';
import { Header, BookInfo } from './Components'
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

class Book extends Component {
    constructor (props) {
        super(props)
        this.state = {bookID: this.props.match.params['bookid']}
    }

    componentDidMount() {
        // state is updated by this time
        console.log(this.state)
    }

    render() {
        return <Fragment>
            <Header />
            <BookInfo bookid={this.state.bookID} />
        </Fragment>
    }
}

export default withStyles(styles)(Book);
