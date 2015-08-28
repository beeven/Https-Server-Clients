#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Author: Beeven Yip
# Written at 2015-08-26

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from OpenSSL import crypto
import datetime
import uuid
import ipaddress
import argparse

one_day = datetime.timedelta(1,0,0)

def make_ca_cert():
    
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend()
    )

    public_key = private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME,u'CN'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Guangdong'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Guangzhou'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Guangzhou Customs'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'IT'),
        x509.NameAttribute(NameOID.COMMON_NAME,u'Guangzhou Customs Certificate Authority'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME,u'CN'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Guangdong'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Guangzhou'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Guangzhou Customs'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'IT'),
        x509.NameAttribute(NameOID.COMMON_NAME,u'Guangzhou Customs Certificate Authority')
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime(2018,8,25))
    builder = builder.serial_number(int((uuid.uuid4())))
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=0), critical=True
    )

    builder = builder.add_extension(
        x509.KeyUsage(
            digital_signature = True,
            content_commitment = True,
            key_encipherment = True,
            data_encipherment = True,
            key_agreement = True,
            key_cert_sign = True,
            crl_sign = True,
            encipher_only = False,
            decipher_only = False
        ),
        critical = False
    )

    builder = builder.add_extension(
        x509.ExtendedKeyUsage([
            x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
            x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
            x509.oid.ExtendedKeyUsageOID.CODE_SIGNING
        ]),
        critical = False
    )
    certificate = builder.sign(
        private_key = private_key,
        algorithm = hashes.SHA256(),
        backend = default_backend()
    )

    ca_key_bytes = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.PKCS8,
        encryption_algorithm = serialization.BestAvailableEncryption(b"mypassword")
    )

    ca_cer_bytes = certificate.public_bytes(serialization.Encoding.PEM)
    return (ca_key_bytes,ca_cer_bytes)


def make_server_csr():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend()
    )
    public_key = private_key.public_key()

    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME,u'CN'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Guangdong'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Guangzhou'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Guangzhou Customs'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'IT'),
        x509.NameAttribute(NameOID.COMMON_NAME,u'Single Window Server'),
    ]))
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )

    builder = builder.add_extension(
        x509.KeyUsage(
            digital_signature = False,
            content_commitment = True,
            key_encipherment = True,
            data_encipherment = True,
            key_agreement = True,
            key_cert_sign = False,
            crl_sign = False,
            encipher_only = False,
            decipher_only = False
        ),
        critical = True
    )

    builder = builder.add_extension(
        x509.ExtendedKeyUsage([
            x509.oid.ExtendedKeyUsageOID.SERVER_AUTH
        ]),
        critical = True
    )

    builder = builder.add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            #x509.DNSName("swdemo.gzeport.net"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            x509.IPAddress(ipaddress.IPv4Address("172.7.1.87")),
            x509.IPAddress(ipaddress.IPv4Address("183.63.251.70"))
        ]),
        critical = False
    )

    request = builder.sign(
        private_key = private_key,
        algorithm = hashes.SHA256(),
        backend = default_backend()
    )

    key_bytes = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )

    csr_bytes = request.public_bytes(serialization.Encoding.PEM)
    return (key_bytes,csr_bytes)


def make_client_csr():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend()
    )
    public_key = private_key.public_key()

    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME,u'CN'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Guangdong'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Guangzhou'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Guangzhou Eport'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'IT'),
        x509.NameAttribute(NameOID.COMMON_NAME,u'SGYClient'),
    ]))
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )

    builder = builder.add_extension(
        x509.KeyUsage(
            digital_signature = True,
            content_commitment = True,
            key_encipherment = False,
            data_encipherment = True,
            key_agreement = True,
            key_cert_sign = False,
            crl_sign = False,
            encipher_only = False,
            decipher_only = False
        ),
        critical = False
    )

    builder = builder.add_extension(
        x509.ExtendedKeyUsage([
            x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH
        ]),
        critical = False
    )

    request = builder.sign(
        private_key = private_key,
        algorithm = hashes.SHA256(),
        backend = default_backend()
    )

    key_bytes = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )

    csr_bytes = request.public_bytes(serialization.Encoding.PEM)
    return (key_bytes,csr_bytes)

def sign_csr_with_ca(caKey, caCert, csr):
    req = x509.load_pem_x509_csr(csr, default_backend())
    ca = x509.load_pem_x509_certificate(caCert, default_backend())
    key = serialization.load_pem_private_key(caKey, b"mypassword", default_backend())
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(req.subject)
    builder = builder.issuer_name(ca.subject)
    builder = builder.public_key(req.public_key())
    builder = builder.serial_number(int(uuid.uuid4()))
    builder = builder.not_valid_before(ca.not_valid_before)
    builder = builder.not_valid_after(ca.not_valid_after)
    for e in req.extensions:
        builder = builder.add_extension(e.value, critical=e.critical)
    cert = builder.sign(
        private_key = key,
        algorithm = hashes.SHA256(),
        backend = default_backend()
    )
    return cert.public_bytes(serialization.Encoding.PEM)

def make_pkcs12(key, cert, caCerts=None):
    pkc = crypto.PKCS12()
    pkc.set_certificate(crypto.load_certificate(crypto.FILETYPE_PEM,cert))
    pkc.set_privatekey(crypto.load_privatekey(crypto.FILETYPE_PEM,key,b"mypassword"))
    if caCerts is not None:
        pkc.set_ca_certificates([crypto.load_certificate(crypto.FILETYPE_PEM,cert) for cert in caCerts])
    pkc_bytes = pkc.export("mypassword")
    return pkc_bytes




def get_predefined_obj(name):
    cacert = b"""-----BEGIN CERTIFICATE-----
MIID+TCCAuGgAwIBAgIRAMd0dg16YU2Wo8MTZn1UD+QwDQYJKoZIhvcNAQELBQAw
gZAxCzAJBgNVBAYTAkNOMRIwEAYDVQQIDAlHdWFuZ2RvbmcxEjAQBgNVBAcMCUd1
YW5nemhvdTEaMBgGA1UECgwRR3Vhbmd6aG91IEN1c3RvbXMxCzAJBgNVBAsMAklU
MTAwLgYDVQQDDCdHdWFuZ3pob3UgQ3VzdG9tcyBDZXJ0aWZpY2F0ZSBBdXRob3Jp
dHkwHhcNMTUwODI3MTU1MzEzWhcNMTgwODI1MDAwMDAwWjCBkDELMAkGA1UEBhMC
Q04xEjAQBgNVBAgMCUd1YW5nZG9uZzESMBAGA1UEBwwJR3Vhbmd6aG91MRowGAYD
VQQKDBFHdWFuZ3pob3UgQ3VzdG9tczELMAkGA1UECwwCSVQxMDAuBgNVBAMMJ0d1
YW5nemhvdSBDdXN0b21zIENlcnRpZmljYXRlIEF1dGhvcml0eTCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAKsfpypj7ihjMaO9/jZ2VdsFoGMGzcTg4pa3
9q7aRS80Z9kITm+nI84FvhrMo3iLCn3WvQrq5vhaVg63ZoTIr9uaNVCKeZgauANS
TT/ddi5BKzDebpBpzNaR7wxp6OY8it6txtCrOHBpJ2caSFqf2zWrhCyJLgxi0Ng8
0/7wEr3+2Yj4Yo6JRm8XRzsYX54SJA9hyWnKf90InRNJG1Wr2FfS8n5H1BuUeCiR
6RwDRcqRlUSpzKIbx0BBvEzyPg7emT06Ah51ZzW/O61o22zeVmW7IRI1juB8Hoov
p1gNhTlFUZXAyFbW/QrbSeHuFcsi+oyy93D/TlS1CA9X7LmXChECAwEAAaNMMEow
EgYDVR0TAQH/BAgwBgEB/wIBADALBgNVHQ8EBAMCAf4wJwYDVR0lBCAwHgYIKwYB
BQUHAwEGCCsGAQUFBwMCBggrBgEFBQcDAzANBgkqhkiG9w0BAQsFAAOCAQEAWel6
26xVZDU6Cpv8ArNRlXdy7vdi83l6XAAis0q5SQY6whBE4rZNjHSzl8rXK2lULjLq
uF2ApzF1exNJJktXbIJi55Una1OCMhiqSlO9nsfsUlZ8oLzYMJr4/CY+pczuFzJp
LZsI17ncVBsdrGHKVMuUbuzI19YW3FohT5YJz+9eiHqVCwZeOEhCx/xgZwRaacxM
Cvb3WVpwTSblb6rxQmmKWPIVu4pVl/+lzD6/v/ucCSzP6l/p2RePNk7vtJH7ni/I
1R+wydziN655+5NVHqARTG91nHLD028riqvO7mNKJk/NMduohCJn7gI8hErWtZid
7341ut2HYJZFzoImSg==
-----END CERTIFICATE-----
"""
    cakey = b"""-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHzBJBgkqhkiG9w0BBQ0wPDAbBgkqhkiG9w0BBQwwDgQIv7hw915o6JACAggA
MB0GCWCGSAFlAwQBKgQQI7rK4Hh5wcawwCkM2SBkDgSCBNDmtSWRS+v9Ame0B4Tp
PNjl9LvgzNDPPAhM1QP7Pg8J7UylouxVUEbZhJck9EwbK6Wu2F/0X4dNiBuUtiS3
soRot8/Ga+1AFATdIlv/p/KybOPoxT3m88AOuvSMH14BQAhk6B41Zs7lkJtzl3QS
Mje9Xde/3s1DzlxnuvA9UiYTCGy5MF9tJZnWqZNNq9JMZ1veTq8Tel1/YFXwnJHt
F0Y3wWUUIukXWcK0dJDrH3XNnahsHxDV4sNh17/Nzn94guHoqusKE8yYNgtI7cvX
T0H+D4QaQjFiiHsu6ZuzqopI2ep13YOuPd7QeCH/cjY5FS18qPjCGl+B/HtDFhb3
kwtwFIeY3idch/O+efzysKpk3PGuvNxyxXrJ5tc58dsvLGwLVm6UxP3xxX/eBMPM
XOZsVoV5npK5g5dC4CK6O11bY6i3vZ/chQsdj4oRzPDzr4HILrpSTZt7bq7cqrk9
ecpUYufwX1WV4T8mISsw6IsS72H+cB2ood82bmVTy4r5ep57PAZuFa6AFVdOQfpn
1eLKIxzrCRxfXWqaxS9vdDWCYw+lbXErQHoBMUMzrY9XDpSjjCkkkgvPkPBEK9Ht
QxvgEV7/0nBouwtb0XDPhA7G9RNfgY4NBIzmbyssSFxA7q0OVeLJxG6IFm2UZCvw
2LjFbTogmkqOJjXXYxV7CJ5aFQzHfhH1e43yCzV0Vlb11YZRSRXDR9+OZUNoU42G
wCexuaKyLpJvCstCzL0lOKowPleewu2doKwCAg+VTvGnIyzmoTdJRTh2gJfrPAYg
8NhK1jopCwZsN2j+GcCEQeL3po6LNP/58crD1/UgEc0auHNhmAWueP65vg6/AEdb
wYinaYHNHV6ubZN+IqONfY21ptnBvzqMewhOFICYFVDCA+RDbu4oCAZ/uEllbYH5
a4Xywr9GCR6MVw2/efQ9IsX+zRoFgXQOMPuQZsrogj0PeNO+vIEU1FnMC1tqS7Ew
5zlQzojZXM8dWYUexJ2j8kQmnkSkV7xV8gF9XGryUzVB+L5y6cv1BRi6YEKQ9HFo
1pQaSkz0f9ceN/nSbw1sAw/wYkwNdIkn/Wm5n9AzTCn7TU2H3KUiI2pjpXY2FJBg
dqEPigET1QdodIg4C/70XPKtwV/k/pCptdwrG32gH+5yqLrbep2jlYLLGmjniZ6W
6aIZy/OMizRMbRbD72sg0xWK/nqV445aOYZrUfXL9EKkLEpjzVU1nhMWdJboikWS
ISPzynNVvJqKRrhHoW2i1Wpy6mjNkCPQEDWRVWt6Hw2zjIqYTtGrgGNpW7xKoNQD
wd/erzMSerOIdCg3QuWQdboqRm6txR1KMYAfXLZjSPiTHmYoM7PpAn99h5bPVT6l
Y9BYnC3pENYlyQ7hHlfujC5BhQtDUGLQrNWbVue80o6M6Lr9vrL6Ct7DhFNEnyIO
t6Jx3w9KO0LV6hMJvR8Bgy0WAoJXuQFCL5uZI4paHFAy7hfdtH20aYU24/cHjV5X
ehfM5CABEbXrttcJHfzzFYwRhPZXZOxeFK6FILrDy4PIdESH9PbMIBkQNG8kNS02
eoCovuCUmw73S3jUQZifVM7z/ODcs5IjNLt4QdXGwD9UlNGYI5l4evxq1n7wfEIj
NbnBmDMlUW05BU0njW4/eUBoTA==
-----END ENCRYPTED PRIVATE KEY-----
"""
    store = {"cacert": cacert, "cakey": cakey}
    return store[name]




if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Make certificates.")
    sub_parsers = parser.add_subparsers(dest='command')

    cert_info_parser = argparse.ArgumentParser(add_help=False)
    cert_info_parser.add_argument("-C", action='store', default='CN')
    cert_info_parser.add_argument("-S", action='store', default='Guangdong')
    cert_info_parser.add_argument("-L", action='store', default='Guangzhou')
    cert_info_parser.add_argument("-O", action='store', default='Guangzhou Customs')
    cert_info_parser.add_argument("-OU", action='store', default='IT')
    cert_info_parser.add_argument("-CN", action='store', default='SGY')
    cert_info_parser.add_argument("-DNS", action='store', nargs="+")
    cert_info_parser.add_argument("-IP", action='store', nargs="+")
    
    ca_parser = sub_parsers.add_parser('ca',description="Make self-signed CA certificate.",parents=[cert_info_parser])
    ca_parser.add_argument("-new",action='store_true', dest="new")
    ca_parser.add_argument('-keyout',type=argparse.FileType('wb'))

    req_parser = sub_parsers.add_parser('req',description="Make server certificates signed by CA.",parents=[cert_info_parser])
    

    x509_parser = sub_parsers.add_parser('x509',parents=[cert_info_parser])
    x509_parser.add_argument('-req', type=argparse.FileType('rb'))
    x509_parser.add_argument('-CA',dest="ca", type=argparse.FileType('rb'))
    x509_parser.add_argument('-CAkey', dest='cakey', type=argparse.FileType('rb'))
    x509_parser.add_argument('-keyout', type=argparse.FileType('wb'))

    args = parser.parse_args()
    print(args)

    if args.command == 'ca':
        if args.new == True:
            cakey, cacert = make_ca_cert()
        else:
            cakey = get_predefined_obj('cakey')
            cacert = get_predefined_obj('cacert')
        if args.keyout is not None:
            args.keyout.write(cakey)
            args.keyout.close()
        print(cacert)
    elif args.command == 'x509':
        if args.ca is not None:
            cacert = args.ca.read()
        else:
            cacert = get_predefined_obj('cacert')
        if args.cakey is not None:
            cakey = args.cakey.read()
        else:
            cakey = get_predefined_obj('cakey')
        if args.req is not None:
            req = args.req.read()
        else:
            svrkey, req = make_server_csr()
            if args.keyout is not None:
                args.keyout.write("svrkey")
                args.keyout.close()
        svrcer = sign_csr_with_ca(cakey,cacert,req)
        print(svrcer)
    elif args.command == 'req':
        pass






    # cakey, cacert = make_ca_cert()
    # svrkey, svrcsr = make_server_csr()
    # svrcert = sign_csr_with_ca(cakey, cacert, svrcsr)
    # clientkey, clientcsr = make_client_csr()
    # clientcert = sign_csr_with_ca(cakey, cacert, clientcsr)

    # with open("ca.cer", "wb") as f:
    #     f.write(cacert)
    # with open("ca.key", "wb") as f:
    #     f.write(cakey)
    # with open("server.cer", "wb") as f:
    #     f.write(svrcert)
    # with open("server.key", "wb") as f:
    #     f.write(svrkey)
    # with open("client.cer", "wb") as f:
    #     f.write(clientcert)
    # with open("client.key", "wb") as f:
    #     f.write(clientkey)
