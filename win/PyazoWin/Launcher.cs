using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PyazoWin {

    class Launcher {

        private enum ProcessDPIAwareness {
            ProcessDPIUnaware = 0,
            ProcessSystemDPIAware = 1,
            ProcessPerMonitorDPIAware = 2
        }

        [DllImport("shcore.dll")]
        private static extern int SetProcessDpiAwareness(ProcessDPIAwareness value);

        private static bool toggleOpenBrowser = true;
        private static bool toggleCopyClipboard = true;

        [STAThread]
        public static int Main(string[] args) {
            foreach (string arg in args) {
                switch (arg) {
                    case "-nb":
                        toggleOpenBrowser = false;
                        break;
                    case "-nc":
                        toggleCopyClipboard = false;
                        break;
                }
            }
            string server = System.AppDomain.CurrentDomain.FriendlyName
                .Replace("Pyazo", "")
                .Replace("_", "")
                .Replace("-", ":")
                .Replace(".exe", "");
            if (server == "") {
                server = "i.beryju.org";
            }
            try {
                if (Environment.OSVersion.Version.Major >= 6) {
                    SetProcessDpiAwareness(ProcessDPIAwareness.ProcessPerMonitorDPIAware);
                }
            } catch (EntryPointNotFoundException) {
                //this exception occures if OS does not implement this API, just ignore it.
            }

            var image = SnippingForm.Snip();
            if (image == null) {
                return 1; // User pressed escape or window was closed
            }
            var client = new PyazoClient(server);
            var url = client.Upload(image);
            if (url == null) {
                return 2; // Some error occured while uploading the image
            }
            if (toggleOpenBrowser) {
                Process.Start(url);
            }
            if (toggleCopyClipboard) {
                Clipboard.SetText(url);
            }
            return 0;
        }

    }
}
