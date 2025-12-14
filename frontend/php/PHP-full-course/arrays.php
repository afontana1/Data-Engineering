<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Associative Arrays</title>
</head>

<body>
    <form action="arrays.php" method="post">
        <input type="text" name="country" placeholder="enter country...">
        <input type="submit" value="capital">
    </form>
</body>

</html>

<?php

//? old way of creating arrays 
// $guitars = array('Strat', 'Les Paul', 'Vela');

//? current way of creating arrays
$guitars = ['Strat', 'Les Paul', 'Vela'];

print_r($guitars);

if (isset($guitars[2])) {
    echo $guitars[2];
} else {
    echo "Guitar does not exist";
}

//? associative arrays
$capitals = array(
    "USA" => "Washington D.C.",
    "Japan" => "Tokyo",
    "South Korea" => "Seoul",
    "India" => "New Delhi"
);

// $country = ucwords($_POST["country"]);
// $capital = $capitals[$country];

// echo "The capital of {$country} is {$capital}";

// $capitals["USA"] = "Las Vegas";
// array_pop($capitals);
// array_shift($capitals);
// $keys = array_keys($capitals);
// $values = array_values($capitals);
// $capitals = array_flip($capitals); // keys and values are swapped
// $capitals = array_reverse($capitals); // array order is reversed
// echo count($capitals);

// foreach ($capitals as $key => $value) {
//     echo "{$key} = {$value} <br>";
// }

foreach ($capitals as $key => $value) {
    echo "{$key} - {$value} <br>";
}