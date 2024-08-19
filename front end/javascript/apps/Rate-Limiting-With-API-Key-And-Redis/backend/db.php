<?php

$host = 'localhost:3306';
$user = 'root';
$pwd = 'root';
$db = 'sakila';

$conn = new mysqli($host, $user, $pwd, $db);
if($conn->connect_errno){
    echo $conn->connect_error;
    exit();
}