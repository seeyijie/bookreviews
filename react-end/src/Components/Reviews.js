import React from 'react';
import { Card, CardHeader, CardContent, Typography, Avatar } from '@material-ui/core';
import axios from 'axios';
import * as config from '../Data/config';

class Reviews extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoading: props.isLoading,
            error: false,
            bookID: this.props.bookID ? this.props.bookID : null,
            reviews: this.props.reviews ? this.props.reviews : [],
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps !== this.props) {
            this.setState({
                isLoading: this.props.isLoading,
                reviews: this.props.reviews ? this.props.reviews : [],
            });
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
                    {this.state.isLoading ? <tr><Typography>Loading reviews...</Typography></tr> : null}
                    {reviews.map(review => <Review data={review} key={review.id} onChange={this.props.onChange}/>)}
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
            isDeleted: false,
            data: this.props.data,
            loggedInID: null,
            token: null,
        }
    }

    componentDidMount() {
        const loggedInID = localStorage.getItem('id')
        const token = localStorage.getItem('jwt')
        this.setState({
            loggedInID: loggedInID,
            token: token,
        });
    }

    onDeleteHandler(id, e) {
        const loggedInID = localStorage.getItem('id')
        const token = localStorage.getItem('jwt')
        
        this.setState({
            isLoading: true,
            loggedInID: loggedInID,
            token: token,
        }, () => {
            // call flask api to delete all logs
            const url = `${config.flaskip}/api/deletereview/` + id
            // const url = `http://127.0.0.1:5000/api/deletereview/` + id
            axios.delete(
                url,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.setState({
                        isLoading: false,
                        isDeleted: true
                    });
                })
                .catch((error) => {
                    this.setState({
                        isLoading: false,
                        isDeleted: false,
                    })
                });
        });
    }

    render() {
        const data = this.state.data;
        if (data == null) return null;

        const { reviewerID, reviewerName, summary, reviewText, reviewTime, id } = data;
        const loggedInID = this.state.loggedInID;

        return (

            this.state.isDeleted ? null :
                <tr style={{ width: '100%' }}>
                    <td style={{ width: '100%' }}>
                        <Card>
                            <CardHeader
                                avatar={
                                    <Avatar>{reviewerName ? reviewerName[0] : ''}</Avatar>
                                }
                                title={reviewerName ? reviewerName : 'Anonymous'}
                                subheader={reviewTime}
                                action={
                                    reviewerID === loggedInID ?
                                        <button disabled={this.state.isLoading} onClick={this.onDeleteHandler.bind(this, id)} value={id}>x<i className="deleteButton"></i>
                                        </button>
                                    : null
                                }
                            />
                            <CardContent>
                                <Typography component='p'><b>{summary}</b></Typography>
                                <Typography component='p'>{reviewText}</Typography>
                            </CardContent>
                        </Card>
                    </td>
                </tr>

        );
    }


}

export default Reviews;