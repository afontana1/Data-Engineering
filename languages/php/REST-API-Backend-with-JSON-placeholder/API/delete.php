<?php
ini_set('display_errors',1);
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET");
 header("Content-Type: application/json; charset=UTF-8");

// if request is not made thorugh HTTP GET method
if ($_SERVER['REQUEST_METHOD'] !=="GET"){
    http_response_code(503);
    echo json_encode(Array(
        "status" => 0,
        "message" => "Incorrect HTTP request method user; access denied!"
    ));
}
// if request is made thorugh HTTP GET method
else{
    
    // If the id of the record to be deleted is not provided
    if (!isset($_GET['id'])){
        http_response_code(503);
        echo json_encode(Array(
        "status" => 0,
        "message" => "No Id provded to delete the respective record; operation aborted!"
    ));
    }
    // If the id of the record to be deleted is provided
    else{
        require "../Resource/Student.php";
        $std = new Student();
        $result = $std->deleteStudent($_GET['id']); 
        // echo $result;
        if ($result)
           {
            http_response_code(200);
            echo json_encode(Array(
            "status" => 1,
            "message" => "Student Record deleted successfully!",
            "result" => $result
             ));
            }
        else{
            http_response_code(500);
            echo json_encode(Array(
            "status" => 0,
            "message" => "Record not found or something went wrong! Deletion unsuccessful!"
             ));
            }
        }

    }
