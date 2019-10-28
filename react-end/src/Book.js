import React, { Component, Fragment } from 'react';
import { Header, BookInfo } from './Components'
import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';

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
    constructor(props) {
        super(props)

        this.state = {
            isLoading: true,
            error: false,
            bookID: this.props.match.params['bookid'],
            categories: null,
            description: null,
            imUrl: null,
            price: null,
            also_viewed: [],
            buy_after_viewing: [],
            sales_rank: null,
            title: null,
        }
    }

    componentDidMount() {
        // call flask api
        // sample asin: B0002IQ15S, 1603420304
        const url = `http://127.0.0.1:5000/api/books/${this.state.bookID}`
        axios.get(url)
            .then(response => response.data)
            .then(book => {
                if (book.book_metadata == null) {
                    this.setState({
                        isLoading: false,
                        error: true,
                    });
                    return;
                }
                return book.book_metadata;
            })
            .then(data => {
                this.setState({
                    isLoading: false,
                    imUrl: data.imUrl,
                    title: data.title,
                    categories: data.categories,
                    sales_rank: data.sales_rank,
                    description: data.description,
                    price: data.price,
                    also_viewed: data.related ? data.related.also_viewed : null,
                    buy_after_viewing: data.related ? data.related.buy_after_viewing : null,
                })
            })
    }

    render() {
        const { bookID, categories, description, imUrl, price, also_viewed, buy_after_viewing, sales_rank, title } = this.state;

        const loadingMessage = <Typography>Loading... Please wait</Typography>
        const errorMessage = <Typography>Error: Book not found</Typography>

        return <Fragment>
            <Header />
            {this.state.isLoading ? loadingMessage : (
                this.state.error ? errorMessage : (
                    <BookInfo bookID={bookID} categories={categories} description={description} imUrl={imUrl} price={price} also_viewed={also_viewed} buy_after_viewing={buy_after_viewing} sales_rank={sales_rank} title={title} />
                )
            )}
        </Fragment>
    }
}

export default withStyles(styles)(Book);
