<?php
include("database.php");

$username = "Megan";
$password = "Space2001";
$hash = password_hash($password, PASSWORD_DEFAULT);

//? INSERTING DATA INTO DB
// $sql = "INSERT INTO users (user, password)
//         VALUES ('$username', '$hash')";

//? RETRIEVING DATA FROM DB
$sql = "SELECT * FROM users";
$result = mysqli_query($connection, $sql);

if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        echo $row["id"] . "<br>";
        echo $row["user"] . "<br>";
        echo $row["password"] . "<br>";
        echo $row["reg_date"] . "<br>";
    }
} else {
    echo "No user found <br>";
}

try {
    mysqli_query($connection, $sql);
    echo "User registered";
} catch (mysqli_sql_exception) {
    echo "Cannot register user";
}

mysqli_close($connection);
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Connection</title>
</head>

<body>
    <p>Test</p>
</body>

</html>