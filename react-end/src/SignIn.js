import React, { Component, Fragment } from 'react';
import Header from "./Components/Header";
import {Grid} from "@material-ui/core";
import Login from "./Components/Login"

class SignIn extends Component {
    render() {
        return (
          <Fragment>
              <Header></Header>
              <Grid container alignItems='center' direction='column'>
                  <Login></Login>
              </Grid>
          </Fragment>
        )
    }
}

export default SignIn;
