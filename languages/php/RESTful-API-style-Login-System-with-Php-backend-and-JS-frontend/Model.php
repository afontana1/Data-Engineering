<?php
// this header needs to set according to where your frontend is running
header("Access-Control-Allow-Origin: http://localhost:5501");

header("Access-Control-Allow-Methods: GET,POST,PUT,PATCH,DELETE");
header('Access-Control-Allow-Credentials: true');
header('Content-Type: plain/text');
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Methods,Access-Control-Allow-Origin, Access-Control-Allow-Credentials, Authorization, X-Requested-With");

include_once "./db.inc.php";
include_once "refactors.inc.php";
session_start();
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    echo 'Welcome to RESTful login System';
    exit();
}
if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['crud_req'] == 'register')
    registerUser($conn);

else if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['crud_req'] == 'login')
    login($conn);

else if ($_SERVER['REQUEST_METHOD'] == 'PUT')
    updateUser($conn);

else if ($_SERVER['REQUEST_METHOD'] == 'DELETE')
    deleteUser($conn);

else if ($_SERVER['REQUEST_METHOD'] == 'GET')
    logout($conn);

// *****************Login function **********************
function login($conn)
{

    $username = $_POST['userName'];
    $pwd = $_POST['pwd'];

    $sql = "select pwd from users where user_name=?;";
    $stmt = $conn->stmt_init();
    if (!$stmt->prepare($sql))
        httpReply(400, "Something went wrong");

    $stmt->bind_param('s', $username);
    if ($stmt->execute()) {
        $result = $stmt->get_result();
        $data = $result->fetch_assoc();
        $isValid = password_verify($pwd, $data['pwd']);
        if ($isValid) {
            $key = password_hash($username, PASSWORD_DEFAULT);
            $_SESSION[$key] = $username;
            setcookie('user', $key);
            http_response_code(200);
            echo 'welcome ' . $username;
        } else {
            http_response_code(401);
            echo "Invalid User name or password";
        }
    }
    exit();
}
// ************Delete User *****************
function deleteUser($conn)
{

    if (!isset($_COOKIE['user'])) {
        http_response_code(403);
        echo "You are not authorized to perform this operation";
        exit();
    }
    $user = $_SESSION[$_COOKIE['user']];

    $sql = "DELETE FROM users where user_name=?;";
    $stmt = $conn->stmt_init();
    if (!$stmt->prepare($sql)) {
        echo 'something went wrong';
        exit();
    }
    $stmt->bind_param('s', $user);
    $stmt->execute();
    if ($stmt->affected_rows > 0)
        echo $user . " is no longer a registered member!!! ";
    exit();
};
// **************** Update User ****************
function updateUser($conn)
{

    if (!isset($_COOKIE['user']))
        httpReply(403, "you are not logged in");

    $sql = "update users set first_name = ?, last_name=?, user_name=?,  email=?, pwd=?, r_pwd=? where user_name=?;";

    $stmt = $conn->stmt_init();

    parse_str(file_get_contents("php://input"), $_PATCH);

    $password = password_hash($_PATCH['pwd'], PASSWORD_DEFAULT);
    $stmt->prepare($sql);
    $stmt->bind_param('sssssss', $_PATCH['fName'], $_PATCH['lName'], $_PATCH['userName'], $_PATCH['email'], $password, $password, $_SESSION[$_COOKIE['user']]);
    if ($stmt->execute()) {
        if ($stmt->affected_rows > 0) {
            $userHash = password_hash($_PATCH['userName'], PASSWORD_DEFAULT);
            $_SESSION[$userHash] = $_PATCH['userName'];
            setcookie('user', $userHash);
            http_response_code(200);
            echo "record updated";
        } else {
            echo 'row not affected';
        }
    }
}

function registerUser($conn)
{

    $fName = $_POST['fName'];
    $lName  = $_POST['lName'];
    $userName = $_POST['userName'];
    $email = $_POST['email'];
    $pwd = $_POST['pwd'];
    $rPwd = $_POST['rPwd'];

    if (empty($fName) || empty($lName) || empty($userName) || empty($pwd) || empty($rPwd)) {
        http_response_code(401);
        echo "All fields need to be filled!!!";
        exit();
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo "bad email address";
        exit();
    }

    if ($pwd != $rPwd) {
        http_response_code(400);
        echo "passwords inconsistent";
        exit();
    }

    $pwd = password_hash($pwd, PASSWORD_DEFAULT);
    $rPwd = password_hash($rPwd, PASSWORD_DEFAULT);



    $sql = "Insert into users (first_name, last_name, user_name, email, pwd, r_pwd) values (?,?,?,?,?,?);";
    $stmt = $conn->stmt_init();
    if (!$stmt->prepare($sql)) {
        echo "smething went wrong!!!";
        exit();
    }
    $stmt->bind_param('ssssss', $fName, $lName, $userName, $email, $pwd, $rPwd);
    $stmt->execute();
    if ($stmt->affected_rows) {
        http_response_code(200);
        echo "Congratulation!!\n Registration successful\n";
    }
    exit();
}

function logout()
{
    if (!isset($_COOKIE['user'])) {
        echo "You are not logged in!!!";
        exit();
    }
    unset($_SESSION['user']);
    session_destroy();
    setcookie('user', false);
    echo "You are logged out!!! " . session_status();
    exit();
}
