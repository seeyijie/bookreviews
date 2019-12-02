import React, {Component} from 'react';
import {Redirect} from 'react-router-dom';
import {TextField, Grid} from '@material-ui/core';
import axios from 'axios';
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Button from "@material-ui/core/Button";
import withStyles from "@material-ui/core/styles/withStyles";
import PropTypes from 'prop-types';
import * as config from '../Data/config';

const useStyles = makeStyles(theme => ({
  '@global': {
    body: {
      backgroundColor: theme.palette.common.white,
    },
  },
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));


class BookForm extends Component {
  constructor(props){
    super(props);
    this.state = {
      title: null,
      salesRank: null,
      price: null,
      description: null,
      imUrl: null,
      categories: null,
      isLoading: false,
      error: false,
      doRedirect: false,
      token: null,
      asin: null, // asin of newly created book if successful
    };
    this.handleClick = this.handleClick.bind(this);
    this.onChange = this.onChange.bind(this)
  }

  componentDidMount() {
    const token = localStorage.getItem('jwt')
    this.setState({
        token: token,
    });
  }

  parseCategories() {
    var categories = this.state.categories;
    if (categories === null) {
      return [];
    } else if (categories === '') {
      return false;
    }

    try {
      categories = categories.split(',');
      return categories;
    } catch {
      return false;
    }
  }

  handleClick(e) {
    const token = localStorage.getItem('jwt')

    const newBook = {
      title: this.state.title || '',
      salesRank: this.state.salesRank || '',
      price: this.state.price || '',
      description: this.state.description || '',
      imUrl: this.state.imUrl || '',
      categories: this.parseCategories(this.state.categories) || [],
      related: {
        also_bought: [],
        also_viewed: [],
        bought_together: [],
      },
    };

    this.setState({
      title: newBook.title,
      salesRank: newBook.salesRank,
      price: newBook.price,
      description: newBook.description,
      imUrl: newBook.imUrl,
      categories: this.state.categories || '',
      isLoading: true,
      token: token,
    }, () => {
      // axios.post(`${config.flaskip}/api/addbook`, newBook)
      axios.post(
        `${config.flaskip}/api/addbook`,
        newBook,
        {
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'Authorization': `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.setState({
            asin: response.data.asin,
            isLoading: false,
            doRedirect: true,
          });
        })
        .catch(err => {
          console.log(err);
          this.setState({
            isLoading: false,
            error: true,
          });
        })
    });
  };

  onChange = e => this.setState({ [e.target.id]: e.target.value });

  render() {
    const {classes} = this.props;
    const {title, description, price, imUrl, categories, asin, isLoading, error } = this.state;

    return (
      <Container component="main" maxWidth="xs" >
        { this.state.doRedirect && <Redirect to={"/books/" + asin} /> }
        <CssBaseline />
          <div className={classes.paper}>
          <Typography component="h1" variant="h5">
            Add Book
          </Typography>
            <br></br>
          <form className={classes.form} noValidate>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  name="title"
                  variant="outlined"
                  required
                  fullWidth
                  id="title"
                  label="Title"
                  value={title}
                  autoFocus
                  error={title === ''}
                  onChange={(e) => {this.setState({title: e.target.value})}}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  required
                  fullWidth
                  id="description"
                  label="Description"
                  name="description"
                  value={description}
                  error={description === ''}
                  onChange={(e) => this.setState({description: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  required
                  fullWidth
                  name="price"
                  label="Price"
                  id="price"
                  value={price}
                  error={isNaN(price) || price === ''}
                  onChange={e => this.setState({price: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  fullWidth
                  id="imUrl"
                  label="Image URL"
                  name="imUrl"
                  value={imUrl}
                  onChange={(e) => this.setState({imUrl: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  required
                  fullWidth
                  id="categories"
                  label="Categories"
                  name="imUrl"
                  value={categories}
                  error={this.parseCategories() === false}
                  helperText="Please provide a comma-separated list of categories"
                  onChange={(e) => this.setState({categories: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
              </Grid>
            </Grid>
            <Button
              fullWidth
              disabled={isLoading}
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={e => this.handleClick()}
            >
              Submit Book
            </Button>
            {error ? (
              <Grid container>
                <Grid item>
                  <Typography variant="caption" style={{color: 'red'}}>
                    Something went wrong. Please try again.
                  </Typography>
                </Grid>
              </Grid>
            ) : null}
          </form>
        </div>
      </Container>
    );
  }
}
BookForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(BookForm);