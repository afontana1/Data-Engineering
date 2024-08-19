<?php
$title = "For Loop";
$favouriteGuitars = ['Vela', 'Explorer', 'Strat'];
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>PHP Fundamentals: <?= $title; ?></title>
    <link href="bootstrap.min.css" rel="stylesheet" />
    <link href="php-fundamentals.css" rel="stylesheet" />
</head>

<body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#">PHP Fundamentals: <?= $title; ?></a>
        </div>
    </nav>

    <div class="container">
        <div class="row">
            <div class="col-lg-12 text-center">
                <h1 class="mt-5"></h1>
            </div>
        </div>
        <div class="row">
            <table class="table table-striped">
                <?php

                for ($i = 0; $i < count($favouriteGuitars); $i++) {
                    $guitar = $favouriteGuitars[$i];
                    echo "<tr><td>$guitar<td></tr>";
                }
                ?>
            </table>
        </div>
    </div>
</body>

</html>