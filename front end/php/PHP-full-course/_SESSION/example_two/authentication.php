<?php

require_once("config.php");

function authenticate_user($email, $password)
{
    return $email == EMAIL && $password == PASSWORD;
}

function is_user_authenticated()
{
    return isset($_SESSION["email"]);
}

function redirect($url)
{
    header("Location: $url");
}

function ensure_user_is_authenticated()
{
    if (!is_user_authenticated()) {
        redirect("login.php");
        die();
    }
}