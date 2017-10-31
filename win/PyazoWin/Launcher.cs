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
            if (!EventLog.SourceExists(EL_SOURCE))
                EventLog.CreateEventSource(EL_SOURCE, EL_LOG);
            EventLog.WriteEntry(EL_SOURCE, String.Format("Pyazo Version {} starting",
                typeof(Launcher).Assembly.GetName().Version.ToString()), EventLogEntryType.Information);

            foreach (string arg in args) {
                switch (arg) {
                    case "-nb":
                        toggleOpenBrowser = false;
                        EventLog.WriteEntry(EL_SOURCE, "Disabling toggleOpenBrowser",
                            EventLogEntryType.Information);
                        break;
                    case "-nc":
                        toggleCopyClipboard = false;
                        EventLog.WriteEntry(EL_SOURCE, "Disabling toggleCopyClipboard",
                            EventLogEntryType.Information);
                        break;
                }
            }
            string server = System.AppDomain.CurrentDomain.FriendlyName
                .Replace("Pyazo", "")
                .Replace("_", "")
                .Replace("-", ":")
                .Replace(".exe", "");
            EventLog.WriteEntry(EL_SOURCE, String.Format("Extracted server {} from filename", server), 
                EventLogEntryType.Information);
            if (server == "") {
                EventLog.WriteEntry(EL_SOURCE, "Fell back to i.beryju.org", EventLogEntryType.Warning);
                server = "i.beryju.org";
            }
            try {
                if (Environment.OSVersion.Version.Major >= 6) {
                    SetProcessDpiAwareness(ProcessDPIAwareness.ProcessPerMonitorDPIAware);
                    EventLog.WriteEntry(EL_SOURCE, "Enable DPI Awareness", EventLogEntryType.Information);
                }
            } catch (EntryPointNotFoundException) {
                EventLog.WriteEntry(EL_SOURCE, "DPI Awareness not supported", EventLogEntryType.Warning);
                //this exception occures if OS does not implement this API, just ignore it.
            }

            var image = SnippingForm.Snip();
            if (image == null) {
                EventLog.WriteEntry(EL_SOURCE, "User canceled snipping", EventLogEntryType.Information);
                return 1; // User pressed escape or window was closed
            }
            var client = new PyazoClient(server);
            var url = client.Upload(image);
            if (url == null) {
                EventLog.WriteEntry(EL_SOURCE, "Failed to upload picture", EventLogEntryType.Error);
                return 2; // Some error occured while uploading the image
            }
            if (toggleCopyClipboard) {
                Clipboard.SetText(url);
                EventLog.WriteEntry(EL_SOURCE, String.Format("Set clipboard to {}", url),
                    EventLogEntryType.Information);
            }
            if (toggleOpenBrowser) {
                Process.Start(url);
                EventLog.WriteEntry(EL_SOURCE, String.Format("Opened url {}", url),
                    EventLogEntryType.Information);
            }
            EventLog.WriteEntry(EL_SOURCE, "Goodbye", EventLogEntryType.Information);
            return 0;
        }

    }
}
