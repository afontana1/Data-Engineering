<?php
class userInfo
{
    private $username;
    private $password;


    public function __construct($formData)
    {
        $this->username = isset($formData["name"]) ? $formData["name"] : null;
        $this->password = isset($formData["password"]) ? $formData["password"] : null;
    }

    public function getUsername()
    {
        return $this->username;
    }

    public function getPassword()
    {
        return $this->password;
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $formData = $_POST;
    $dataInstance = new UserInfo($formData);

    $username = $dataInstance->getUsername();
    $password = $dataInstance->getPassword();

    echo "ALL DATA:" . "<br>";
    echo "USERNAME: {$username}" . "<br>";
    echo "PASSWORD: {$password}";
}