<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] !='POST')
{echo 'Request not received through post method. Aborting!!!'; return;}

require "../Resource/Student.php";
$data = json_decode(file_get_contents("php://input"));

if (empty($data->name) || empty($data->email) || empty($data->class) || empty($data->gender))
{   http_response_code(404);
    $data = json_encode(Array(
        "status" => 0,
        "message" => "incomplete data provided. Aborting operation!"
    ));
     echo $data;
}
else{
$name = $data->name;
$email = $data->email;
$class = $data->class;
$gender = $data->gender;

$std = new Student();

$status = $std->createStudent($name, $email, $class, $gender);
if ($status){
    http_response_code(200);
    $data = json_encode(Array(
        "status" => 1,
        "message" => "Student Added Successfully!"
    ));
    echo $data;
}
else
{
http_reponse_code(500);
$data = json_encode(Array(
    "status" => 0,
    "message" => "Something went wrong!\nOperation Aborted!"
));
echo $data;
}
}

