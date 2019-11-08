import React, { Component, Fragment } from 'react';
import { Header, BookInfo } from './Components'
import Reviews from "./Components/Reviews.js"
import { Grid, Typography } from '@material-ui/core';
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
    },
    loadtext: {
        marginTop: '50px',
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
            reviews: [],
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
                console.log(book);

                const reviews = book.reviews;
                const data = book.book_metadata;
                this.setState({
                    isLoading: false,
                    imUrl: data.imUrl,
                    title: data.title,
                    categories: data.categories,
                    sales_rank: data.sales_rank,
                    description: data.description,
                    price: data.price,
                    also_bought: data.related ? (data.related.also_bought ? data.related.also_bought : []) : [],
                    also_viewed: data.related ? (data.related.also_viewed ? data.related.also_viewed : []) : [],
                    buy_after_viewing: data.related ? (data.related.buy_after_viewing ? data.related.buy_after_viewing : []) : [],
                    reviews: reviews ? reviews : [],
                })
            })
    }

    render() {
        const { bookID, categories, description, imUrl, price, also_viewed, buy_after_viewing, sales_rank, title, reviews } = this.state;
        // console.log(reviews)
        const { classes } = this.props
        const loadingMessage = <Typography className={classes.loadtext}>Loading... Please wait</Typography>
        const errorMessage = <Typography className={classes.loadtext}>Error: Book not found</Typography>

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                {this.state.isLoading ? loadingMessage : (
                    this.state.error ? errorMessage : (
                        <div>
                            <BookInfo bookID={bookID} categories={categories} description={description} imUrl={imUrl} price={price} also_viewed={also_viewed} buy_after_viewing={buy_after_viewing} sales_rank={sales_rank} title={title} />
                            <br />
                            <div style={{ width: '90%', margin: 'auto' }}>
                                <p>Reviews:</p>
                                <Reviews reviews={reviews} />
                            </div>
                        </div>
                    )
                )}
            </Grid>
        </Fragment>
    }
}

export default withStyles(styles)(Book);
