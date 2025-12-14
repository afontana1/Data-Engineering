<?php

require "../dbh/Database.php";

class Student{
    private $name;
    private $email;
    private $class;
    private $admission;
    private $gender;
    private $id;
    private $conn;
    private $dbtable;
    
    public function __construct(){
        $db = new Database();
        $this->conn = $db->connect();
    }

public function createStudent($name, $email, $class, $gender){
    $stmt = $this->conn->prepare('insert into student (name, email, class, gender) values(?, ?, ?, ?);');
    $stmt->bind_param("ssss",$name, $email, $class, $gender);
    if($stmt->execute()){
        return true;
    }
    else return false;
}

public function getAllStudents(){
    $stmt ='select * from student;';
    $result = $this->conn->query($stmt);
    // if ($result->num_rows > 0){

    // }
    return $result;
}
public function getStudent($id){
    $stmt = $this->conn->prepare('select * from student where id =?;');
    $stmt->bind_param('i',$id);
     $stmt->execute();
     $result = $stmt->get_result();
    return $result->fetch_assoc();

}

public function updateStudent($id, $name, $email, $class, $gender){
$query = ('update student set name=?, email=?, class=?, gender=? where id=?');
$stmt = $this->conn->prepare($query);
$stmt->bind_param('ssssi', $name, $email, $class, $gender , $id);
if($stmt->execute()){
    return true;
}
else{return false;}
}


public function deleteStudent($id){
    $query="delete from student where id =?";
    $stmt = $this->conn->prepare($query);
    $stmt->bind_param('i',$id);
    $stmt->execute();
    if ($stmt->affected_rows > 0)
        return true;
    else    
        return false;
}
}