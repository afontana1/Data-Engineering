<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkboxes</title>
</head>

<body>

    <form action="checkboxes.php" method="post">
        <input type="checkbox" name="foods[]" value="Pizza">Pizza<br>
        <input type="checkbox" name="foods[]" value="Hamburger">Hamburger<br>
        <input type="checkbox" name="foods[]" value="Hotdog">Hotdog<br>
        <input type="checkbox" name="foods[]" value="Tacos">Tacos<br>
        <input type="submit" name="submit" value="submit">
    </form>

</body>

</html>

<?php
if (isset($_POST["submit"])) {

    if (isset($_POST["foods"]) && is_array($_POST["foods"])) {
        $foods = $_POST["foods"];

        if (!empty($foods)) {
            foreach ($foods as $food) {
                echo "You like {$food}" . "<br>";
            }
        } else {
            echo "Please choose an option";
        }
    } else {
        echo "Please choose an option";
    }
}