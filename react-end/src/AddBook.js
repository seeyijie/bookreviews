import React, { Component, Fragment } from 'react';
import Header from "./Components/Header";
import {Grid} from "@material-ui/core";
import BookForm from "./Components/BookForm"
import Box from "@material-ui/core/Box";

class AddBook extends Component {
    render() {
        return (
          <Fragment>
              <Header/>
              <Box p={2} bgcolor="background.paper" />
              <Grid container alignItems='center' direction='column'>
                  <BookForm/>
              </Grid>
          </Fragment>
        )
    }
}

export default AddBook;
