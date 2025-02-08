<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sanitize / Validate Inputs</title>
</head>

<body>

    <form action="sanitize_validate_inputs.php" method="post">
        <input type="text" placeholder="enter username" name="username"><br>
        <input type="text" placeholder="enter age" name="age"><br>
        <input type="text" placeholder="enter email" name="email"><br>
        <input type="submit" name="login">
    </form>

</body>

</html>

<?php
if (isset($_POST["login"])) {
    //? SANITIZE
    $username = filter_input(INPUT_POST, "username", FILTER_SANITIZE_SPECIAL_CHARS);
    $age = filter_input(INPUT_POST, "age", FILTER_SANITIZE_NUMBER_INT);
    $email = filter_input(INPUT_POST, "email", FILTER_SANITIZE_EMAIL);

    // echo "{$username} is logged in.";
    // echo "You are {$age} years old.";
    // echo "Your email is $email.";

    //? VALIDATE
    $age = filter_input(INPUT_POST, "age", FILTER_VALIDATE_INT);  // if a valid number is not entered an empty string will be returned
    $email = filter_input(INPUT_POST, "email", FILTER_VALIDATE_EMAIL); // if a valid email is not entered an empty string will be returned

    // if (empty($age)) {
    //     echo "Age input not valid";
    // } else {
    //     echo "You are $age years old.";
    // }

    if (empty($email)) {
        echo "Invalid email address";
    } else {
        echo "Your email is $email";
    }
}