<?php
session_start();
session_unset();
session_destroy();

require_once("authentication.php");

redirect("login.php");
die();