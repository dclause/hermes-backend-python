Add here your own certificates.

The easiest way is to use `https://github.com/FiloSottile/mkcert` :

You can generate appropriate files via the following commands:
`mkcert -key-file privatekey.pem -cert-file certificate.pem example.com *.example.com`

```
cd certfiles
openssl genrsa -out privatekey.pem 2048
openssl req -new -key privatekey.pem -out certrequest.csr
openssl x509 -req -in certrequest.csr -signkey privatekey.pem -out certificate.pem
```
