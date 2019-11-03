import React from 'react';
import { Card, CardHeader, CardActions, CardContent, Typography, Avatar } from '@material-ui/core';

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
        if (reviews == null || reviews.length == 0) {
            return <p>No reviews for this product yet.</p>;
        }
        return (
            <table style={{width:'100%'}}>
                {reviews.map(review => <Review data={review} />)}
            </table>
        );
    }

}

class Review extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            data: this.props.data,
        }
    }

    render() {
        const data = this.state.data;
        if (data == null) return null;

        const {reviewerName, summary, reviewText, reviewTime} = data;
        return (
            <tr style={{width:'100%'}}>
                <td style={{width:'100%'}}>
                    <Card>
                        <CardHeader
                            avatar={
                                <Avatar>{reviewerName ? reviewerName[0] : ''}</Avatar>
                            }
                            title={reviewerName ? reviewerName : 'Anonymous'}
                            subheader={reviewTime}
                        />  
                        <CardContent>
                            <Typography component='p'>{summary}</Typography>
                            <Typography component='p'>{reviewText}</Typography>
                        </CardContent>
                    </Card>
                </td>
            </tr>
        );
    }

}

export default Reviews;