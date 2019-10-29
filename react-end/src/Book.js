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
            .then(response => {
                const imUrl = response.data.book_metadata.imUrl
                const title = response.data.book_metadata.title
                const categories = response.data.book_metadata.categories
                const sales_rank = response.data.book_metadata.sales_rank
                const description = response.data.book_metadata.description
                const price = response.data.book_metadata.price
                const also_viewed = response.data.book_metadata.related.also_viewed
                const buy_after_viewing = response.data.book_metadata.related.buy_after_viewing
                return [imUrl, title, categories, sales_rank, description, price, also_viewed, buy_after_viewing]
            })
            .then((array) => {
                this.setState({
                    isLoading: false,
                    imUrl: array[0],
                    title: array[1],
                    categories: array[2],
                    sales_rank: array[3],
                    description: array[4],
                    price: array[5],
                    also_viewed: array[6],
                    buy_after_viewing: array[7],
                })
            })
    }

    render() {
        const { bookID, categories, description, imUrl, price, also_viewed, buy_after_viewing, sales_rank, title } = this.state;

        const loadingMessage = <Typography>Loading... Please wait</Typography>

        return <Fragment>
            <Header />
            {this.state.isLoading ? loadingMessage : <BookInfo bookID={bookID} categories={categories} description={description} imUrl={imUrl} price={price} also_viewed={also_viewed} buy_after_viewing={buy_after_viewing} sales_rank={sales_rank} title={title} />}
        </Fragment>
    }
}

export default withStyles(styles)(Book);
