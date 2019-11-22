import React from 'react';
import { Card, CardHeader, CardContent, TextField, Button, Typography, Avatar } from '@material-ui/core';
import axios from 'axios';
import * as config from '../Data/config';

class ReviewForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            bookID: props.bookID,
            isLoading: false,
            successful: null,
            reviewerID: null,
            reviewerName: null,
            token: null,
        }
    }

    componentDidMount() {
        const reviewerID = localStorage.getItem('id')
        const reviewerName = localStorage.getItem('name');
        const token = localStorage.getItem('jwt')
        this.setState({
            reviewerID: reviewerID,
            reviewerName: reviewerName,
            token: token,
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

        // re-authorize since user may have signed out since component last rendered
        const reviewerID = localStorage.getItem('id')
        const reviewerName = localStorage.getItem('name');
        const token = localStorage.getItem('jwt')

        const {bookID, summary, reviewText} = this.state;
        const url = `${config.flaskip}/api/addreview`;
        // const url = 'http://127.0.0.1:5000/api/addreview';

        this.setState({
            isLoading: true,
            successful: null,
        }, () => {
            axios.post(
                url,
                {
                    asin: bookID,
                    reviewerID: reviewerID,
                    summary: summary,
                    reviewText: reviewText,
                },
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.setState({
                        summary: '',
                        reviewText: '',
                        reviewerID: reviewerID,
                        reviewerName: reviewerName,
                        token: token,
                        isLoading: false,
                        successful: true,
                    });
                    this.props.onChange();
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
        if (reviewerID === null || reviewerID === '') {
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
                            {successful ?
                                <Typography variant='caption' style={{color:'green'}}>Review submitted.</Typography>
                                : (successful === false ?
                                    <Typography variant='caption' style={{color:'red'}}>Something went wrong. Please refresh and try again.</Typography>
                                    : null)
                            }
                        </form>
                    </CardContent>
                </Card>
            </div>
        )
    }

}

export default ReviewForm;