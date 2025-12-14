<?php
//?     hashing - transforming sensitive data (password) into letters, numbers, and/or symbols via a mathematical process (similar to encryption).
//?               Hides the original data from 3rd parties.

$password = "example123";

$hash = password_hash($password, PASSWORD_DEFAULT);

if (password_verify("example123", $hash)) {
    echo "You are logged in!";
} else {
    echo "Incorrect password!";
}