using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PyazoWin {

    class Launcher {

        public static int Main(string[] args) {
            string server = System.AppDomain.CurrentDomain.FriendlyName.Replace("PyazoWin_", "").Replace(".exe", "");
            var image = SnippingForm.Snip();
            if (image == null) {
                return 1; // User pressed escape or window was closed
            }
            var client = new PyazoClient(server);
            var url = client.Upload(image);
            if (url == null) {
                return 2; // Some error occured while uploading the image
            }
            Process.Start(url);
            return 0;
        }

    }
}
