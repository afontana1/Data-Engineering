<?php
session_start();
require_once("authentication.php");

$authenticated_email = $_SESSION["email"];
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homepage</title>
</head>

<body>
    <div>Welcome back <?= $authenticated_email; ?></div>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae molestiae ipsam veniam recusandae, velit accusamus
        rerum quae exercitationem aperiam placeat reprehenderit vero minus nemo beatae hic unde! Harum, eaque
        consequuntur.</p>
</body>

</html>