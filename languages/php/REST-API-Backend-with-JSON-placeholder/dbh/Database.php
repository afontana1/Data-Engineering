<?php
class Database{
    private $host="localhost:3306";
    private $db="hwtdb";
    private $user="root";
    private $pwd="root";
    private $conn;

    public function connect(){
        $this->conn = new mysqli($this->host,$this->user,$this->pwd,$this->db);
        if ($this->conn->connect_error){
            die('Connection Error ' . $this->conn->errno) ;
        }
        else{
            return $this->conn;
        }
    }
}