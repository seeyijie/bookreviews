import React from 'react';
import { Link } from 'react-router-dom'
import { Card, CardHeader, CardContent, TextField, Button, Typography, Avatar } from '@material-ui/core';
import axios from 'axios';

class ReviewForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            bookID: props.bookID,
            isLoading: false,
            successful: false,
            revewerID: null,
            reviewerName: null,
        }
    }

    componentDidMount() {
        const reviewerID = 123; // we should get the ID from localStorage instead (need to figure out how to do this)
        const reviewerName = localStorage.getItem('data');
        this.setState({
            reviewerID: reviewerID,
            reviewerName: reviewerName,
        });
    }

    handleSummaryChange = (event) => {
        this.setState({summary: event.target.value});
    }

    handleReviewTextChange = (event) => {
        this.setState({reviewText: event.target.value});
    }

    handleSubmit = (event) => {
        event.preventDefault();

        const {bookID, summary, reviewText, reviewerID, reviewerName} = this.state;
        const url = 'http://127.0.0.1:5000/api/addreview';

        this.setState({
            isLoading: true,
        }, () => {
            axios.post(
                url,
                {
                    asin: bookID,
                    reviewerID: reviewerID,
                    reviewerName: reviewerName,
                    summary: summary,
                    reviewText: reviewText,
                },
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                })
                .then(response => {
                    console.log(response);
                    this.setState({
                        summary: '',
                        reviewText: '',
                        isLoading: false,
                        successful: true,
                    });
                })
                .catch(error => {
                    console.log(error);
                    this.setState({
                        isLoading: false,
                        successful: false,
                    })
                });
        })
    }

    render() {
        const {summary, reviewText, reviewerID, reviewerName, isLoading, successful} = this.state;
        // we should actually check if reviewerID is set once we figure out how to retrieve it
        if (reviewerName === null || reviewerName === '') {
            return (
                <div style={{ width: '100%', paddingBottom: '30px'}}>
                    <Typography><b><a href="/signin">Sign in</a> to leave a review.</b></Typography>
                </div>
            );
        }

        return (
            <div style={{ width: '100%', border: '2px', padding: '2px'}}>
                <Card>
                    <CardContent>
                        <Typography><b>Write a review</b></Typography>
                    </CardContent>
                    <CardHeader
                        avatar={
                            <Avatar>{reviewerName ? reviewerName[0] : ''}</Avatar>
                        }
                        title={reviewerName}
                        subheader={reviewerID}
                    />
                    <CardContent>
                        <form>
                            <TextField
                                id='summary'
                                label='Summary'
                                value={summary}
                                margin='dense'
                                variant='outlined'
                                disabled={isLoading}
                                onChange={this.handleSummaryChange}
                                fullWidth
                            />
                            <TextField
                                id='reviewText'
                                label='Review Text'
                                value={reviewText}
                                margin='dense'
                                variant='outlined'
                                disabled={isLoading}
                                onChange={this.handleReviewTextChange}
                                fullWidth
                                multiline
                                rows='3'
                            />
                            <Button size='small' color='primary' onClick={this.handleSubmit}>Submit</Button>
                            {successful ? <Typography variant='caption' style={{color:'green'}}>Review submitted.</Typography> : null}
                        </form>
                    </CardContent>
                </Card>
            </div>
        )
    }

}

export default ReviewForm;