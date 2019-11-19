import React from 'react';
import { Card, CardHeader, CardContent, TextField, Button, Typography, Avatar } from '@material-ui/core';
import axios from 'axios';

class ReviewForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            bookID: props.bookID,
            reviewerID: 'replace this ID',
            reviewerName: 'replace this name',
        }
    }

    handleSummaryChange = (event) => {
        this.setState({summary: event.target.value});
    }

    handleReviewTextChange = (event) => {
        this.setState({reviewText: event.target.value});
    }

    handleSubmit = (event) => {
        console.log("submitting");
        event.preventDefault();

        const {bookID, reviewerID, reviewerName, summary, reviewText} = this.state;
        const url = 'http://127.0.0.1:5000/api/addreview/'

        axios.post(url, {
            asin: bookID,
            reviewerID: reviewerID,
            reviewerName: reviewerName,
            summary: summary,
            reviewText: reviewText,
        }, {
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => console.log(response))
            .catch(error => console.log(error));

    }

    render() {
        return (
            <div style={{ width: '100%', border: '2px', padding: '2px'}}>
                <Card>
                    <CardContent>
                        <Typography><b>Write a review</b></Typography>
                    </CardContent>
                    <CardHeader
                        avatar={
                            <Avatar>{}</Avatar>
                        }
                        title={'Your Name'}
                        subheader={'new review'}
                    />
                    <CardContent>
                        <form>
                            <TextField
                                id='summary'
                                label='Summary'
                                margin='dense'
                                variant='outlined'
                                onChange={this.handleSummaryChange}
                                fullWidth
                            />
                            <TextField
                                id='reviewText'
                                label='Review Text'
                                margin='dense'
                                variant='outlined'
                                onChange={this.handleReviewTextChange}
                                fullWidth
                                multiline
                                rows='3'
                            />
                            <Button size='small' color='primary' onClick={this.handleSubmit}>Submit</Button>
                        </form>
                    </CardContent>
                </Card>
            </div>
        )
    }

}

export default ReviewForm;