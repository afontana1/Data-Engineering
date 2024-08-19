<?php
require "../Resource/Student.php";

header('Access-Control-Allow-Methods: GET');
header ('Access-Control-Allow-Origin: *');
header ('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD']=="GET"){
    if (!empty($_GET['id'])){
        $std = new Student();
        $data = $std->getStudent($_GET['id']);
    //    print_r($data);
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
            "message" => " No student id provided; hence operation aborted!"
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
