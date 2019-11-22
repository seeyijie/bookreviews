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
        textTransform: "none"
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
    const isAuth = !!localStorage.getItem('jwt');
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

    function logout() {
        localStorage.clear();
        window.location = '/';
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
            {
                isAuth ?
                    <div>
                        <Button className={classes.button}
                            color="inherit"
                            href="/addbook">
                            Add Book
                        </Button>
                        <Button className={classes.button}
                            color="inherit"
                            onClick={logout}>
                            Logout
                        </Button>
                    </div>
                        : (<div>
                                <Button className={classes.button}
                                 color="inherit"
                                 href="/signin">
                                    Login
                                </Button>
                                <Button className={classes.button}
                                        color="inherit"
                                        href="/signup">
                                    Register
                                </Button>
                            </div>)
            }
        </Toolbar>
    </AppBar>
}

export default Header;