import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom'
import { Header, BookInfo } from './Components'
import Reviews from "./Components/Reviews.js"
import ReviewForm from "./Components/ReviewForm.js"
import { Grid, Typography, Button } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';
import * as config from './Data/config';

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
            isLoadingReviews: true,
            error: false,
            errorReviews: false,
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
        this.fetchMetaData();
        this.fetchReviews();
    }

    fetchMetaData() {
        // sample asin: B0002IQ15S, 1603420304
        const url = `${config.flaskip}/api/books/${this.state.bookID}`
        // const url = `http://127.0.0.1:5000/api/books/${this.state.bookID}`
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

                //const reviews = book.reviews;
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
                })
            })
    }

    fetchReviews() {
        const url = `${config.flaskip}/api/books/${this.state.bookID}/reviews`
        // const url = `http://127.0.0.1:5000/api/books/${this.state.bookID}/reviews`
        axios.get(url)
            .then(response => response.data)
            .then(data => {
                if (data.reviews == null) {
                    this.setState({
                        isLoadingReviews: false,
                        errorReviews: true,
                    });
                    return;
                }

                const reviews = data.reviews;
                this.setState({
                    isLoadingReviews: false,
                    reviews: reviews ? reviews : [],
                })
            })

    }

    handleChange = () => {
        // re-render reviews when a new review is submitted
        this.setState({
            isLoadingReviews: true,
        }, () => this.fetchReviews());
    }

    render() {
        const { bookID, categories, description, imUrl, price, also_bought, also_viewed, buy_after_viewing, sales_rank, title, reviews } = this.state;
        const { classes } = this.props
        const loadingMessage = <Typography className={classes.loadtext}>Loading... Please wait</Typography>
        const errorMessage = <Typography style={{color:'red'}} className={classes.loadtext}>Error: Book not found</Typography>
        const reviewErrorMessage = <Typography style={{color:'red'}} className={classes.loadtext}>Error: Could not retrieve reviews</Typography>

        return <Fragment>
            <Header />
            <Grid container alignItems='center' direction='column'>
                <Link to="/browse" style={{ textDecoration: 'none', alignSelf: 'baseline', paddingLeft: '50px' }}>
                    <Button className={classes.button} variant="contained">
                        Return to browse all books
                    </Button>
                </Link>
                {this.state.isLoading ? loadingMessage : (
                    this.state.error ? errorMessage : (
                        <div>
                            <BookInfo bookID={bookID} categories={categories} description={description} imUrl={imUrl} price={price} also_bought={also_bought} also_viewed={also_viewed} buy_after_viewing={buy_after_viewing} sales_rank={sales_rank} title={title} />
                            <br />
                            <div style={{ width: '90%', margin: 'auto' }}>
                                <h3>Reviews:</h3>
                                <ReviewForm bookID={bookID} onChange={this.handleChange}/>
                                {this.state.errorReviews ? reviewErrorMessage : (
                                    <Reviews reviews={reviews} onChange={this.handleChange} isLoading={this.state.isLoadingReviews}/>
                                )}
                            </div>
                        </div>
                    )
                )}
            </Grid>
        </Fragment>
    }
}

export default withStyles(styles)(Book);
