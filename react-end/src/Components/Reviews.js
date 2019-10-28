import React from 'react';

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
            <table style={{width:'80%', align:'center', border:'1px'}}>
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
        console.log(data)
        if (data == null) return null;

        const {reviewerID, reviewerName, summary, reviewText, reviewTime} = data;
        return (
            <tr>
                <td>
                    <tr>
                        <th>Author:</th>
                            <td>{reviewerName}</td>
                        <th>ID:</th>
                            <td>{reviewerID}</td>
                        <th>Time:</th>
                            <td>{reviewTime}</td>
                    </tr>
                    <tr>
                        <th>Summary:</th>
                            <td>{summary}</td>
                    </tr>
                    <tr>
                        <th>Text:</th>
                            <td>{reviewText}</td>
                    </tr>
                </td>
            </tr>
        );
    }

}

export default Reviews;