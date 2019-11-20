import React, { Component, Fragment } from 'react';
import Header from "./Components/Header";
import Register from "./Components/Register";
import {Grid} from "@material-ui/core";
import Box from "@material-ui/core/Box";

class SignUp extends Component {
    render() {
        return (
          <Fragment>
              <Header></Header>
              <Box p={2} bgcolor="background.paper" />
              <Grid container alignItems='center' direction='column'>
                  <Register></Register>
              </Grid>
          </Fragment>
        )
    }
}


export default SignUp;
