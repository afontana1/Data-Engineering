<?php
require "../Resource/Student.php";

header('Access-Control-Allow-Methods: POST');
header ('Access-Control-Allow-Origin: *');
header ('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD']=="POST"){
$param = json_decode(file_get_contents('php://input'));
if (!empty($param->id)){
    $std = new Student();
   $data = $std->getStudent($param->id);

if (!empty($data)){
    http_response_code(200);
    echo json_encode(array(
        "status" => 1,
        "data" => $data
    ));
}
else{
    http_response_code(404);
    echo json_encode(array(
        'status' => 0,
        "message" => 'student not found'
    ));
}

}
else{
    http_response_code(503);
    echo json_encode(array(
        "status" => 0,
        "message" => "Access denied!"
    ));
}
}
else{
    http_response_code(503);
    echo json_encode(Array(
        "status" => 0,
        "mesage" => "invalid method used; access denied!"
    ));
}
