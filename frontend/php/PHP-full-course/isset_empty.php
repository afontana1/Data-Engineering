<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>isset() and empty()</title>
</head>

<body>
    <form action="isset_empty.php" method="post">
        <input type="text" placeholder="enter username..." name="username"><br>
        <input type="password" placeholder="enter password..." name="password"><br>
        <input type="submit" value="Log In" name="login">
    </form>
</body>

</html>

<?php
//? isset() and empty()
//? isset() = returns TRUE if a variable is declared and not null
//? empty() = returns TRUE if a variable is not declared, false, null, ""

foreach ($_POST as $key => $value) {
    echo "{$key} = {$value} <br>";
}

if (isset($_POST["login"])) {

    $username = $_POST["username"];
    $password = $_POST["password"];

    if (empty($username)) {
        echo "Username is missing";
    } elseif (empty($password)) {
        echo "Password is missing";
    } else {
        echo "Welcome back {$username}";
    }
}