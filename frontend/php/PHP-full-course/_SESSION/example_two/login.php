<?php
session_start();
$title = "Session Login";
require_once("authentication.php");

//? user is redirected to homepage if already authenticated
if (is_user_authenticated()) {
    redirect("homepage.php");
    die();
}

//? submit user information for authentication
if (isset($_POST["login"]) && $_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_input(INPUT_POST, "email", FILTER_VALIDATE_EMAIL);
    $password = filter_input(INPUT_POST, "password", FILTER_SANITIZE_SPECIAL_CHARS);

    // compare with data store
    if (authenticate_user($email, $password)) {
        $_SESSION["email"] = $email;
        $_SESSION["password"] = $password;
        redirect("homepage.php");
        die();
    } else {
        $status = "Please enter the correct information";
    }

    if ($email == false) {
        $status = "Please enter a valid email address";
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title><?= $title; ?></title>
    <link href="../../assets/bootstrap.min.css" rel="stylesheet" />
    <link href="../../assets/php-fundamentals.css" rel="stylesheet" />
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#"><?= $title; ?></a>
        </div>
    </nav>
    <form action="" method="POST">
        <input type="text" name="email" placeholder="enter email"><br>
        <input type="password" name="password" placeholder="enter password"><br>
        <input type="submit" name="login" value="login">
    </form>
    <div>
        <?php
        if (isset($status)) {
            echo $status;
        }
        ?>
    </div>
</body>

</html>