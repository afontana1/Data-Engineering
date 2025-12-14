<?php
$db_server = "localhost:3307";
$db_user = "root";
$db_password = "";
$db_name = "businessdb";
$connection = "";

try {
    $connection = mysqli_connect($db_server, $db_user, $db_password, $db_name);
    if (!$connection) {
        throw new Exception("Could not connect to database");
    }
    echo "Connected to database <br>";
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "<br>";
}