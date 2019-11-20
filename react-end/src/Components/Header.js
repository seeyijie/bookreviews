import React from 'react';
import { Link, useHistory } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, InputBase } from '@material-ui/core';
import { fade, makeStyles } from '@material-ui/core/styles';
import SearchIcon from '@material-ui/icons/Search';

const useStyles = makeStyles(theme => ({
    title: {
        marginRight: theme.spacing(2)
    },
    button: {
        marginRight: theme.spacing(2),
    },
    blankspace: {
        flexGrow: 1
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(3),
            width: 'auto',
        },
    },
    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: 200,
        },
    },
}));

function Header() {

    const classes = useStyles();
    let history = useHistory();

    function handleSearch(e) {
        if (e.key === 'Enter') {
            history.push({
                pathname: '/searchresults/' + e.target.value.replace(/ /g, '+'),
                state: {
                    isSearch: true,
                    searchstring: e.target.value.replace(/ /g, '+')
                }
            });
        }
    }

    function redirectToLogin() {
        history.push('/signin');
    }

    function redirectToSignup() {
        history.push('/signup');
    }

    return <AppBar position="static">
        <Toolbar>
            <Link to="/" style={{ textDecoration: 'none', color: 'white' }}>
                <Typography className={classes.title} variant="subtitle1" color='inherit'>
                    Book Review Database
             </Typography>
            </Link>
            <div className={classes.search}>
                <div className={classes.searchIcon}>
                    <SearchIcon />
                </div>
                <InputBase
                    placeholder="Search"
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                    inputProps={{ 'aria-label': 'search' }}
                    onKeyDown={handleSearch}
                />
            </div>
            <div className={classes.blankspace}></div>
                <Button className={classes.button}
                        color="inherit"
                        href="/signin"
                >
                    LOGIN
                </Button>
                <Button className={classes.button}
                        color="inherit"
                        href="/signup"
                >
                    REGISTER
                </Button>
        </Toolbar>
    </AppBar>
}

export default Header;