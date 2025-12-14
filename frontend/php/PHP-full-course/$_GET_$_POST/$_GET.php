<?php
$title = "_GET";

//? If an integer is not inserted it returns false
$category = filter_input(INPUT_GET, "category", FILTER_SANITIZE_SPECIAL_CHARS); // sanitizing input
$limit = filter_input(INPUT_GET, "limit", FILTER_VALIDATE_INT); // validating input

// die(); kills the application if condition is false
// if ($category == false || $limit == false) {
//     die();
// }

if ($category == false) {
    $category = 1;
}

if ($limit == false) {
    $limit = 10;
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?></title>
</head>

<body>

    <p>CATEGORY: <?= $category ?>, LIMIT: <?= $limit ?></p>
</body>

</html>