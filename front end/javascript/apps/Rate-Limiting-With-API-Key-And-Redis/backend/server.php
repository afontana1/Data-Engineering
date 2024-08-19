<?php

require './db.php';
require './../vendor/autoload.php';

$redisClient = new Predis\Client();
$ttl;
$array = array();

if($_SERVER['REQUEST_METHOD']=='GET'){
    $ip = $_SERVER['REMOTE_ADDR'];
    $reqCount = $redisClient->incr($ip);
    if($reqCount == 1) $redisClient->expire($ip, 20);
    if($reqCount < 6){
      $result = $conn->query('select  * from actor;');
      if($result->num_rows){
          while($row = $result->fetch_assoc())
           array_push($array, $row );
        echo json_encode($array) ;
        exit();   
      }
      else{
        echo json_encode(['status'=>"No data found!!!"]);
        exit();
      }       
    }
    else{
        $ttl = $redisClient->ttl($ip);
        echo json_encode(['status'=>"you have used up yuor alloted quota. Try again after {$ttl} seconds."]);
    }

}








?>