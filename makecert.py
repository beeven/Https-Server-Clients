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
    x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1"))
    ]),
    critical = False
)

builder = builder.add_extension(
    x509.KeyUsage(
        digital_signature = True,
        content_commitment = False,
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

pkc = crypto.PKCS12()
pkc.set_certificate(crypto.load_certificate(crypto.FILETYPE_PEM,ca_cer_bytes))
pkc.set_privatekey(crypto.load_privatekey(crypto.FILETYPE_PEM,ca_key_bytes,b"mypassword"))
pkc_bytes = pkc.export("mypassword")
with open("ca.pfx","wb") as f:
    f.write(pkc_bytes)
