<?php
session_start();
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homepage</title>
</head>

<body>
    <h2>This is the Homepage</h2>
    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Officiis vel mollitia quia reprehenderit maiores
        ratione nam cumque, omnis ad totam velit quas est in, quidem exercitationem vitae quos perspiciatis numquam.
        Beatae mollitia, delectus amet doloremque, iste ducimus debitis distinctio ex voluptatibus laboriosam sapiente
        vitae cum incidunt neque repellendus odio totam molestias nesciunt? Error, nam accusantium! Itaque natus placeat
        dolorum incidunt ex eaque sequi ut quisquam velit? Sint nostrum cupiditate minus aperiam repudiandae sunt
        laudantium autem nemo, enim illo quo consequatur voluptas optio assumenda perferendis dolore expedita explicabo
        qui quisquam! Numquam consequuntur esse nostrum earum commodi? Voluptates fuga in veniam porro!</p>

    <form action="home.php" method="post">
        <input type="submit" name="logout" value="logout">
    </form>
</body>

</html>

<?php
echo $_SESSION["username"] . "<br>";
echo $_SESSION["password"] . "<br>";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    session_destroy();
    header("Location: index.php");
}