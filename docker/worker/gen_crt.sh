cd /etc/ssl/certs/

if [ ! -f casm_web.csr ]; then
  openssl req -new -newkey rsa:2048 -sha256 -nodes -out casm_web.csr -keyout \
casm_web.key -subj "/C=CN/ST=Shanghai/L=Shanghai/O=Example Inc./OU=Web Security/CN=127.0.0.1"
fi

if [ ! -f casm_web.crt ]; then
  openssl x509 -req -days 3650 -in casm_web.csr -signkey casm_web.key -out casm_web.crt
fi
