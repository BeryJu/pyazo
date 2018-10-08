using SharpRaven;
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

        public const string EL_SOURCE = "pyazo";
        public const string EL_LOG = "Application";

        [STAThread]
        public static int Main(string[] args) {
            AppDomain currentDomain = AppDomain.CurrentDomain;
            currentDomain.UnhandledException += new UnhandledExceptionEventHandler(RavenHandler);

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
            } catch (DllNotFoundException) {
                //this exception occures if OS does not implement this API, just ignore it.
            }

            var image = SnippingForm.Snip();
            if (image == null) {
                return 1; // User pressed escape or window was closed
            }
            var client = new PyazoClient(server);
            var url = client.Upload(image, Environment.UserName);
            if (url == null) {
                return 2; // Some error occured while uploading the image
            }
            if (toggleCopyClipboard) {
                Clipboard.SetText(url);
            }
            if (toggleOpenBrowser) {
                Process.Start(url);
            }
            return 0;
        }

        static void RavenHandler(object sender, UnhandledExceptionEventArgs args) {
            Exception e = (Exception)args.ExceptionObject;
            var ravenClient = new RavenClient("https://dfcc6acbd9c543ea8d4c9dbf4ac9a8c0:5340ca78902841b5b3372ecce5d548a5@sentry.services.beryju.org/4");
            ravenClient.Capture(new SharpRaven.Data.SentryEvent(e));
        }

    }
}
