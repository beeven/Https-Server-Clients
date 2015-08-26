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
        x509.NameAttribute(NameOID.COMMON_NAME,u'CA'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME,u'CN'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Guangdong'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Guangzhou'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Guangzhou Customs'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'IT'),
        x509.NameAttribute(NameOID.COMMON_NAME,u'CA')
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
        x509.NameAttribute(NameOID.COMMON_NAME,u'SGYServer'),
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
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Guangzhou Customs'),
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
    if cacerts is not None:
        pkc.set_ca_certificates([crypto.load_certificate(crypto.FILETYPE_PEM,cert) for cert in caCerts])
    pkc_bytes = pkc.export("mypassword")
    return pkc_bytes





if __name__=="__main__":
    cakey, cacert = make_ca_cert()
    svrkey, svrcsr = make_server_csr()
    svrcert = sign_csr_with_ca(cakey, cacert, svrcsr)
    clientkey, clientcsr = make_client_csr()
    clientcert = sign_csr_with_ca(cakey, cacert, clientcsr)

    with open("ca.cer", "wb") as f:
        f.write(cacert)
    with open("ca.key", "wb") as f:
        f.write(cakey)
    with open("server.cer", "wb") as f:
        f.write(svrcert)
    with open("server.key", "wb") as f:
        f.write(svrkey)
    with open("client.cer", "wb") as f:
        f.write(clientcert)
    with open("client.key", "wb") as f:
        f.write(clientkey)
