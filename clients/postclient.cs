using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Security.Cryptography.X509Certificates;
using System.IO;
using System.Net.Security;

namespace PostClient
{
    class Program
    {
        static void Main(string[] args)
        {
            var clientCertData = File.ReadAllBytes(@"C:\Users\Beeven\Desktop\aspnet\certs\client.pfx");
            //var caCertData = File.ReadAllBytes(@"C:\Users\Beeven\Desktop\aspnet\certs\ca.cer");
            X509Certificate2 clientCert = new X509Certificate2(clientCertData, "beeven");
            //X509Certificate2 caCert = new X509Certificate2(caCertData);
            HttpWebRequest req = WebRequest.CreateHttp("https://localhost:8080/");
            req.ClientCertificates.Add(clientCert);
            req.Method = "POST";
            req.ServerCertificateValidationCallback =
                (object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors) =>
                {
                    Console.WriteLine(certificate.Subject);
                    return true;
                };
            req.ContentType = "application/json; charset=utf-8";
            var reqstream = req.GetRequestStream();
            StreamWriter sw = new StreamWriter(reqstream);
            sw.Write("{\"Hello\":\"World!\"}");
            sw.Close();


            var res = req.GetResponse() as HttpWebResponse;
            Console.WriteLine(res.StatusDescription);
            Stream resstream = res.GetResponseStream();
            StreamReader sr = new StreamReader(resstream);
            var data = sr.ReadToEnd();
            sr.Close();
            resstream.Close();
            res.Close();

            reqstream.Close();

            Console.ReadKey();
        }
    }
}
