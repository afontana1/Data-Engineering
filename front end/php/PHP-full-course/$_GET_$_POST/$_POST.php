<?php
$title = "_POST";

if (isset($_POST["login"]) && $_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_input(INPUT_POST, "email", FILTER_VALIDATE_EMAIL);

    if ($email == false) {
        $status = "Please enter a valid email address";
    }

    foreach ($_POST as $data) {
        echo $data . "<br>";
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?= $title; ?></title>
    <link href="../assets/bootstrap.min.css" rel="stylesheet" />
    <link href="../assets/php-fundamentals.css" rel="stylesheet" />
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-lg-12 text-center">
                <h1 class="mt-5"></h1>
            </div>
        </div>
        <div class="row">
            <form action="" method="POST">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input class="form-control" type="text" name="email" id="email">
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input class="form-control" type="password" name="password" id="password">
                </div>
                <div class="form-group">
                    <input type="submit" name="login" value="login">
                </div>
            </form>
        </div>
        <div class="row">
            <?php
            if (isset($status)) {
                echo $status;
            }
            ?>
        </div>
    </div>
</body>

</html>