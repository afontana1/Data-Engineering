<?php
	// trying to do everything as simple as possible, so...

	if (isset($_SERVER['HTTP_ORIGIN'])) {
		header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
		header('Access-Control-Allow-Credentials: true');
		header('Access-Control-Max-Age: 86400');
	}
	if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
		if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
			header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         
		if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
			header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
		exit(0);
	}
	header('Content-Type: application/json');
	
	session_start();
	include "conn.php";
	
	$apiResult['code'] = 500;
	$apiResult['data'] = "empty request";
	$apiResult['success'] = false;
	
	function apiResponse($code, $data, $success = false){
		$apiResult['code'] = $code;
		$apiResult['data'] = $data;
		$apiResult['success'] = $success;
		echo json_encode($apiResult);
	}

	$sql = "SELECT * FROM tbl WHERE id='1'";
	$result = $conn->query($sql);
	if ($result->num_rows > 0) {
		$row = $result->fetch_assoc();
		$sql = "UPDATE tbl SET name='new name' WHERE id='1'";
		if($conn->query($sql) === TRUE)
			return apiResponse(200, $row, true);
		else
			return apiResponse(500, ['msg' => $conn->error]);
		
	} else
		return apiResponse(404, ['msg' => 'no rows found']);

	apiResponse(200, "hello world", true);
	
	$conn->close();
