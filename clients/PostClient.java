
import org.apache.http.HttpHost;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.ssl.DefaultHostnameVerifier;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.HttpContext;
import org.apache.http.ssl.SSLContexts;
import org.apache.http.ssl.TrustStrategy;

import javax.net.ssl.SSLContext;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.security.*;
import java.security.cert.*;
import java.security.cert.Certificate;
import java.util.Date;
import java.util.Set;


/**
 * Created by Beeven on 8/12/2015.
 */
public class postclient {

    public static void main(String[] args) throws Exception{
        KeyStore clientKeyStore = KeyStore.getInstance("PKCS12");
        clientKeyStore.load(new FileInputStream("C:\\Users\\Beeven\\Desktop\\aspnet\\certs\\client.pfx"), "beeven".toCharArray());
        KeyStore trustKeyStore = KeyStore.getInstance("PKCS12");
        trustKeyStore.load(null);
        CertificateFactory factory = CertificateFactory.getInstance("x509");
        Certificate cacert = factory.generateCertificate(new FileInputStream("C:\\Users\\Beeven\\Desktop\\aspnet\\certs\\ca.cer"));
        trustKeyStore.setCertificateEntry("ca",cacert);


        SSLContext sslContext = SSLContexts.custom()
                .loadKeyMaterial(clientKeyStore,"beeven".toCharArray())
                .loadTrustMaterial(trustKeyStore,null)
                .build();
        SSLConnectionSocketFactory sslsf = new SSLConnectionSocketFactory(
                sslContext, new DefaultHostnameVerifier()
        );

        HttpClient client = HttpClients.custom()
                .setSSLSocketFactory(sslsf)
                .build();

        HttpPost post = new HttpPost("https://localhost:8080/");
        post.setHeader("Content-Type","application/json");
        post.setEntity(new StringEntity("{\"Hello\":\"World!\"}"));
        HttpResponse response = client.execute(post);
        System.out.println(response.getStatusLine().getReasonPhrase());
    }

}
