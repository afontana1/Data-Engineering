<?php
ini_set('display_errors',1);
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Content-Type: application/json; charset=UTF-8");

if($_SERVER['REQUEST_METHOD']==="POST"){
    $params = json_decode(file_get_contents("php://input"));

    // if all or some the data to be updated is missing
    if (empty($params->id) || empty($params->name) || empty($params->email) || empty($params->class) || empty($params->gender))
        {
            http_response_code(503);
            echo json_encode(Array(
                "status" => 0,
                "message" => "please provide data for all the fileds!"
            ));
        }
        else{
            require "../Resource/Student.php";
            $std = new Student();
            $result = $std->updateStudent($params->id, $params->name,$params->email,$params->class, $params->gender);
            if ($result){
                http_response_code(200);
                echo json_encode(Array(
                    "status" => 1,
                    "message" => "student record updated successfully!"
                ));
            }
            else{
                http_response_code(500);
                echo json_encode(Array(
                    "status" => 0,
                    "message" => "student record could not be updated!"
                ));

            }
        }

} 
else{
    http_response_code(404);
    echo json_encode(Array(
        "status" => 0,
        "message" => "Service unavailable for the provided HTTP Method "
    ));
}
