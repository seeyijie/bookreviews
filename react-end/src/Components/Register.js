import React, {Component} from 'react';
import {Redirect} from 'react-router-dom';
import {TextField, Grid} from '@material-ui/core';
import axios from 'axios';
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import withStyles from "@material-ui/core/styles/withStyles";
import PropTypes from 'prop-types';
import Link from "@material-ui/core/Link";
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


class Register extends Component {
  constructor(props){
    super(props);
    this.state = {
      name:'',
      email:'',
      password:'',
      doRedirect: false
    };
    this.handleClick = this.handleClick.bind(this);
    this.onChange = this.onChange.bind(this)
  }

  handleClick(e){
    const newUser = {
      email: this.state.email,
      name: this.state.name,
      password: this.state.password
    };
    console.log(newUser);
    axios.post(`${config.flaskip}/register`, newUser)
    // axios.post('http://127.0.0.1:5000/register', newUser)
      .then(res => this.setState({ doRedirect: true}))
      .catch(err => console.log(err));
  };

  onChange = e => this.setState({ [e.target.id]: e.target.value });

  render() {
    const {classes} = this.props;
    const {name, email, password} = this.state;

    return (
      <Container component="main" maxWidth="xs" >
        { this.state.doRedirect && <Redirect to="/signin" /> }
        <CssBaseline />
          <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
            <br></br>
          <form className={classes.form} noValidate>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  autoComplete="name"
                  name="name"
                  variant="outlined"
                  required
                  fullWidth
                  id="name"
                  label="Name"
                  value={name}
                  autoFocus
                  onChange={(e) => {
                    this.setState(this.onChange(e))
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => {
                    this.setState(this.onChange(e))
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={e => {
                    this.setState(this.onChange(e))
                  }}
                />
              </Grid>
              <Grid item xs={12}>
              </Grid>
            </Grid>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={e => this.handleClick()}
            >
              Sign Up
            </Button>
            <Grid container justify="flex-end">
              <Grid item>
                <Link href="/signin" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
      </Container>
    );
  }
}
Register.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(Register);


// Higher-order component API
// https://material-ui.com/styles/basics/#higher-order-component-api

