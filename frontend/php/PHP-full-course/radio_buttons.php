<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radio Buttons</title>
</head>

<body>
    <form action="radio_buttons.php" method="post">
        <input type="radio" name="credit_card" value="Visa">Visa<br>
        <input type="radio" name="credit_card" value="Mastercard">Mastercard<br>
        <input type="radio" name="credit_card" value="American Express">American Express<br>
        <input type="submit" name="submit_card" value="choose payment">
    </form>
</body>

</html>

<?php
if (isset($_POST["submit_card"])) {
    $credit_card = null;
    if (isset($_POST["credit_card"])) {
        $credit_card = $_POST["credit_card"];
        $card_type = "";
        switch ($credit_card) {
            case "Visa":
                $card_type = "Visa";
                break;
            case "Mastercard":
                $card_type = "Mastercard";
                break;
            case "American Express":
                $card_type = "American Express";
                break;
        }
        echo "You chose {$card_type}";
    } else {
        echo "Please choose a card";
    }
}