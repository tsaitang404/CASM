db.user.drop()
db.user.insert({ username: 'admin',  password: hex_md5('casmsalt!@#'+'casm@pass') })