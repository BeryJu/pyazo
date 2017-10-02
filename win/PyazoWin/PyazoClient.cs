using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Mime;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PyazoWin {

    public class PyazoClient {

        public string endpoint = "http://localhost:8000/upload/";

        public PyazoClient(string server) {
            this.endpoint = string.Format("https://{0}/upload/", server);
        }

        public string Upload(Image image) {
            using (var client = new HttpClient())
            using (var mfdc = new MultipartFormDataContent())
            using (var ms = new MemoryStream())
            using (var filecontent = new StreamContent(ms)) {
                image.Save(ms, ImageFormat.Png);
                ms.Seek(0, SeekOrigin.Begin);

                filecontent.Headers.ContentDisposition =
                  new ContentDispositionHeaderValue(DispositionTypeNames.Attachment) {
                      FileName = "image.png",
                      Name = "imagedata"
                  };
                filecontent.Headers.ContentType = new MediaTypeHeaderValue("image/png");

                mfdc.Add(filecontent);
                mfdc.Add(new StringContent("foo"), "id");
                try {
                    var res = client.PostAsync(endpoint, mfdc).Result;
                    return res.Content.ReadAsStringAsync().Result;
                } catch (AggregateException ae) {
                    MessageBox.Show(ae.Flatten().ToString());
                    return null;
                }
            }
        }

    }

}
