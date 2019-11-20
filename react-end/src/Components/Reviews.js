import React from 'react';
import { Card, CardHeader, CardContent, Typography, Avatar } from '@material-ui/core';
import axios from 'axios';
import * as config from '../Data/config';

class Reviews extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoading: true,
            error: false,
            bookID: this.props.bookID ? this.props.bookID : null,
            reviews: this.props.reviews ? this.props.reviews : [],
        }
    }

    render() {
        const reviews = this.state.reviews;
        if (reviews == null || reviews.length === 0) {
            return <p>No reviews for this product yet.</p>;
        }
        return (
            <table style={{ width: '100%' }}>
                <tbody>
                    {reviews.map(review => <Review data={review} />)}
                </tbody>
            </table>
        );
    }

}

class Review extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoading: false,
            data: this.props.data,
        }
    }
    onDeleteHandler(id, e) {
        // call flask api to delete all logs
        const url = `${config.flaskip}/api/deetereview/` + id
        // const url = `http://127.0.0.1:5000/api/deletereview/` + id
        axios.delete(url)
        this.setState({
            isLoading: true
        })
    }
    componentDidMount() {
        // call flask api
        // sample asin: B0002IQ15S, 1603420304
        if (this.state.isLoading === true) {
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
                    // const data = book.book_metadata;
                    this.setState({
                        isLoading: false,
                        reviews: reviews ? reviews : [],
                    })
                })
        }
    }

    render() {
        const data = this.state.data;
        if (data == null) return null;

        const { reviewerName, summary, reviewText, reviewTime, id } = data;
        return (

            this.state.isLoading ? null :
                <tr style={{ width: '100%' }}>
                    <td style={{ width: '100%' }}>
                        <Card>
                            <CardHeader
                                avatar={
                                    <Avatar>{reviewerName ? reviewerName[0] : ''}</Avatar>
                                }
                                title={reviewerName ? reviewerName : 'Anonymous'}
                                subheader={reviewTime}
                            />
                            <CardContent>
                                <Typography component='p'><b>{summary}</b></Typography>
                                <Typography component='p'>{reviewText}</Typography>
                                <button onClick={this.onDeleteHandler.bind(this, id)} value={id}>delete comment{id}<i className="deleteButton"></i>
                                </button>
                            </CardContent>
                        </Card>
                    </td>
                </tr>

        );
    }


}

export default Reviews;