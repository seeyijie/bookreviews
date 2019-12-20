import React, {Component} from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import axios from "axios";
import {Redirect} from "react-router-dom";
import setAuthToken from "../util/setAuthToken";
import * as config from '../Data/config';
import {emails, passwords} from "../util/credentialsEnum";


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
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));


class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
      doRedirect: false,
      isLoading: false,
      passwordValidation: passwords.INIT,
      emailValidation: emails.INIT
    };
    this.handleClick = this.handleClick.bind(this);
    this.onChange = this.onChange.bind(this)
  }

  handleClick(e){
    if (this.state.password.length >= 5) {
      this.setState({
        passwordValidation: passwords.VALID
      });
    } else if (0 < this.state.password.length < 5) {
      this.setState({
        passwordValidation: passwords.INVALID
      });
    }

    if (this.state.email.match('(\\w+\\.)*\\w+@(\\w+\\.)+[A-Za-z]+')) {
      this.setState({
        emailValidation: emails.VALID
      });
    } else {
      this.setState({
        emailValidation: emails.INVALID
      })
    }
    const user = {
      email: this.state.email,
      password: this.state.password
    };

    this.setState({isLoading: true});
    axios.post(`${config.flaskip}/login`, user)
    // axios.post('http://127.0.0.1:5000/login', user)
      .then(res => res.data.data)
      .then(data => {
        localStorage.setItem('jwt', data.access_token);
        localStorage.setItem('id', data.id);
        localStorage.setItem('name', data.name);
        setAuthToken(data.access_token);
        this.setState({ doRedirect: true})
      })
      .catch(err => {
        this.setState({
          errors: err.response.data,
          isLoading: false
        });
      });
  };

  onChange = e => this.setState({ [e.target.id]: e.target.value });

  render() {
    const {classes} = this.props;
    const {email, password, isLoading, emailValidation, passwordValidation} = this.state;

    return (
      <Container component="main" maxWidth="xs">
        { this.state.doRedirect && <Redirect to="/browse" /> }
        <CssBaseline/>
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon/>
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <form className={classes.form} noValidate>
            <TextField
              variant="outlined"
              margin="normal"
              disabled={isLoading}
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              error={emailValidation===emails.INVALID ? "Input a valid email" : null}
              onChange={e => this.setState(this.onChange(e))}
            />
            <TextField
              variant="outlined"
              margin="normal"
              disabled={isLoading}
              error={passwordValidation===passwords.INVALID ? "Password length is incorrect" : null}
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={e => this.setState(this.onChange(e))}
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary"/>}
              label="Remember me"
            />
            <Button
              fullWidth
              disabled={isLoading}
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={e => this.handleClick()}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item>
                <Link href="/signup" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
        <Box mt={8}>
        </Box>
      </Container>
    );
  }
}

Login.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(Login);
