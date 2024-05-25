<?php
include("database.php")
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Project</title>
</head>

<body>
    <form action="<?php htmlspecialchars($_SERVER["PHP_SELF"]) ?>" method="post">
        <h2>Welcome to the Forum</h2>
        <input type="text" placeholder="username..." name="username"><br>
        <input type="password" placeholder="password..." name="password"><br>
        <input type="submit" value="register" name="submit">
    </form>
</body>

</html>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = filter_input(INPUT_POST, "username", FILTER_SANITIZE_SPECIAL_CHARS);
    $password = filter_input(INPUT_POST, "password", FILTER_SANITIZE_SPECIAL_CHARS);

    if (empty($username)) {
        echo "Please enter a username";
    } elseif (empty($password)) {
        echo "Please enter a password";
    } else {
        $hash = password_hash($password, PASSWORD_DEFAULT);
        $sql = "INSERT INTO registered_users (user, password)
                VALUES ('$username', '$hash')";
        try {
            mysqli_query($conn, $sql);
            echo "You are now registered";
        } catch (mysqli_sql_exception) {
            echo "User already registered";
        }
    }
}

mysqli_close($conn);
?>