import React, { Component, Fragment } from 'react';
import Header from "./Components/Header";
import {Grid} from "@material-ui/core";
import Login from "./Components/Login"
import Box from "@material-ui/core/Box";

class SignIn extends Component {
    render() {
        return (
          <Fragment>
              <Header/>
              <Box p={2} bgcolor="background.paper" />
              <Grid container alignItems='center' direction='column'>
                  <Login/>
              </Grid>
          </Fragment>
        )
    }
}

export default SignIn;
