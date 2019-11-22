var db = connect('127.0.0.1:27017/50043_db');

db.createUser({
    user: '50043_user',
    pwd: 'password',
    roles: [{ role: 'readWrite', db:'50043_db'}]
})

