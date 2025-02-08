<?php
$server = "localhost:3306";
$user = "YOUR_DB'S_USERNAME";
$pwd = "YOUR_DB'S_PASSWORD";
$db = "login";

$conn = new mysqli($server, $user, $pwd, $db);

 header("Content-Type: text/html");
if($conn->connect_errno)
{http_response_code(400);
    echo  $conn->connect_error; exit();}
