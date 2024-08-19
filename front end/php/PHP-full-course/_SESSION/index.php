<?php
session_start()
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sessions - Login Page</title>
</head>

<body>
    <form action="index.php" method="post">
        <input type="text" name="username" placeholder="enter username"><br>
        <input type="password" name="password" placeholder="enter password"><br>
        <input type="submit" name="login" value="login">
    </form>
    <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nemo, iste!</p>
</body>

</html>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (!empty($_POST["username"]) && !empty($_POST["password"])) {
        $_SESSION["username"] = $_POST["username"];
        $_SESSION["password"] = $_POST["password"];

        header("Location: home.php");

        echo $_SESSION["username"] . "<br>";
        echo $_SESSION["password"] . "<br>";
    } else {
        echo "username/password not entered";
    }
}