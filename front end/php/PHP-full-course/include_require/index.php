<?php
$title = "Home";
include("header.html");
require_once("functions.php");

$guitars = [
    ['name' => 'Vela', 'manufacturer' => 'PRS'],
    ['name' => 'Explorer', 'manufacturer' => 'Gibson'],
    ['name' => 'Strat', 'manufacturer' => 'Fender']
];

$guitar_names = pluck($guitars, "name");

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?></title>
</head>

<body>
    <h1>This is the <?= $title ?> page</h1>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. <br>
        Magnam necessitatibus corrupti excepturi ea rerum <br>
        voluptatum neque voluptate vitae quaerat! Similique!</p>
    <hr>
    <?php
    outputGuitars($guitar_names);
    ?>
</body>

</html>

<?php
include("footer.html");
?>

<?php
//? include () - Copies the content of a file (php/html/text) and includes it in given php file.
//?              Sections of our website become reusable.
//?              Changes only need to be made in one place.
//? require () - Used to include an external file into PHP script.
//?              If the specified file cannot be found or there is an error while including it, a fatal error is generated, and the script execution is halted.
//?              If require is used multiple times to include the same script file, it will be included each time.
//? require_once() - Also includes an external file into PHP script but with one key difference, it checks if the file has already been included. If it has, it won't include the file again. This prevents problems that may arise from redefining functions or classes and reduces the risk of errors.
