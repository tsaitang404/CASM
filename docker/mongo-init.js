db.user.drop()
db.user.insert({ username: 'casm',  password: hex_md5('casmsalt!@#'+'casm@MongoDB') })