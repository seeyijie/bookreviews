import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
    root: {
        width: '100%',
    },
    paper: {
        marginTop: theme.spacing(3),
        width: '100%',
        overflowX: 'auto',
        marginBottom: theme.spacing(2),
    },
    table: {
        minWidth: 650,
    },
}));

function createData(timestamp, method, url, response) {
    return { timestamp, method, url, response };
}

function generaterows(log_json) {
    const rows = []
    for (var log of log_json.log_json) {
        rows.push(createData(log.timestamp, log.method, log.url, log.response))
    }
    return rows
}

function Logtable({ log_json }) {
    const classes = useStyles();

    const rows = generaterows({ log_json })

    return (
        <div className={classes.root}>
            <Paper className={classes.paper}>
                <Table className={classes.table} size="small" aria-label="a dense table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Timestamp</TableCell>
                            <TableCell align="right">Method</TableCell>
                            <TableCell align="right">URL</TableCell>
                            <TableCell align="right">Response</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows.map(row => (
                            <TableRow>
                                <TableCell component="th" scope="row">
                                    {row.timestamp}
                                </TableCell>
                                <TableCell align="right">{row.method}</TableCell>
                                <TableCell align="right">{row.url}</TableCell>
                                <TableCell align="right">{row.response}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>
        </div>
    );
}

export default Logtable;