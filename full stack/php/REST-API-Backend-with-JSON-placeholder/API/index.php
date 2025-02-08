
<?php
ini_set('display_errors',1);
 header("Access-Control-Allow-Origin: *");
 header("Access-Control-Allow-Methods: GET");
 header("Content-Type: application/json; charset=UTF-8");
 
    if ($_SERVER['REQUEST_METHOD'] === "GET"){
        
        require '../Resource/Student.php';
        $students = Array();

        $std = new Student();          
        $rows = $std->getAllStudents();
     
     if($rows->num_rows > 0){
        while ($row = $rows->fetch_assoc()){
            array_push($students, Array(
             "id" => $row['id'],
                "name" => $row['name'],
                "class" => $row['class'],
                "gender" => $row['gender'],
                "email" => $row['email'],
                "admission_date" => $row['admission_date'],
            ));
         }
         http_response_code(200);
         $data = json_encode(Array(
             "status" => 1,
             "data" => $students
         ));
         echo $data;
 
     }
     else{
         http_response_code(200);
         echo json_encode(Array(
             "status" => 1 ,
             "message" => "No student records found!."
         ));

     }

    }
    else{
        http_response_code(503);
        echo json_encode(Array(
            "status" => 0,
            "message" => "Access Denied!"
        ));
    }
         
          
    ?>
