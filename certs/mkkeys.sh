#echo Creating CA private key
#certtool --generate-privkey --outfile ca-key.pem
#
#echo Creating CA cert
#certtool --template ca.template --generate-self-signed --load-privkey ca-key.pem --outfile ca-cert.pem

echo Creating private key
certtool --generate-privkey --outfile server-key.pem

echo Creating cert
certtool --template server.template --generate-certificate --load-privkey server-key.pem --outfile server-cert.pem --load-ca-certificate ca-cert.pem --load-ca-privkey ca-key.pem

echo Creating private key
certtool --generate-privkey --outfile client-key.pem

echo Creating cert
certtool --template server.template --generate-certificate --load-privkey client-key.pem --outfile client-cert.pem --load-ca-certificate ca-cert.pem --load-ca-privkey ca-key.pem

cat server-cert.pem ca-cert.pem > server.pem
