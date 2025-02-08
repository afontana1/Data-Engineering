<?php
$title = "Scope";

$message = "Welcome everyone";

function output($greeting = "Hello")
{
    global $message, $message_two, $message_three;
    $greeting = $message;
    echo $greeting;
}

function outputGuitars($guitar)
{
    echo '<pre>';
    print_r($guitar);
    echo '<pre>';
}

$guitars = [
    ['name' => 'Vela', 'manufacturer' => 'PRS'],
    ['name' => 'Explorer', 'manufacturer' => 'Gibson'],
    ['name' => 'Strat', 'manufacturer' => 'Fender']
];

// $guitar_name = array_column($guitars, 'manufacturer');

function pluck($arr, $key)
{
    $guitar = array_map(function ($arr) use ($key) {
        return $arr[$key];
    }, $arr);

    return $guitar;
}

$guitar_names = pluck($guitars, "manufacturer");

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?></title>
</head>

<body>
    <?php
    output() //? Welcome everyone
    ?>
    <?php
    outputGuitars($guitar_names);
    ?>
</body>

</html>