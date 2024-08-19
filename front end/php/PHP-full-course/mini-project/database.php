<?php
$db_server = "localhost:3307";
$db_user = "root";
$db_password = "";
$db_name = "businessdb";
$conn = "";

try {
    $conn = mysqli_connect($db_server, $db_user, $db_password, $db_name);
    if (!$conn) {
        throw new Exception("Could not connect to database");
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "<br>";
}