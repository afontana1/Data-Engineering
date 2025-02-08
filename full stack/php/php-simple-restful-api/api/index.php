<?php
/*
* Create a file called .htaccess and copy the following text to it
* change /api to the folder and path that your file is at
*
*
* RewriteEngine On
* RewriteBase /api
* RewriteCond %{REQUEST_FILENAME} !-d
* RewriteCond %{REQUEST_FILENAME} !-f
* RewriteRule ^(.+)$ index.php [QSA,L]
*/
/*
 * Read the Json file
 * This is supposedly our database
 * if we really have a database here we can get the connection
 * and then get all the data from database
 * since we don't have a database
 * we write and get all the data from users.json file
 */
$jsonFile = 'users.json';
// read the file
$data = file_get_contents($jsonFile);
// convert the json to array
$users = json_decode($data, true);

/*
 * get the request method and request uri to handle the requests
 */
$uri = $_SERVER['REQUEST_URI'];   // /api/users
$method = $_SERVER['REQUEST_METHOD'];  // GET,POST,DELETE, etc.

switch ($method | $uri) {
    /*
    * Path: GET /api/users
    * Task: show all the users
    */
    case ($method == 'GET' && $uri == '/api/users'):
        // our response is in Json format
        header('Content-Type: application/json');
        // JSON_PRETTY_PRINT helps the json file be more readable
        echo json_encode($users, JSON_PRETTY_PRINT);
        break;
    /*
    * Path: GET /api/users/{id}
    * Task: get one user
    */
    case ($method == 'GET' && preg_match('/\/api\/users\/[1-9]/', $uri)):
        header('Content-Type: application/json');
        // basename gives the last part of the uri
        // for example in api/users/10 it returns 10
        $id = basename($uri);
        if (!array_key_exists($id, $users)) {
            // user with this id doesn't exists
            // send a 404 response with error messaage
            http_response_code(404);
            echo json_encode(['error' => 'user does not exist']);
            break;
        }
        $responseData = [$id => $users[$id]];
        echo json_encode($responseData, JSON_PRETTY_PRINT);
        break;
    /*
    * Path: POST /api/users
    * Task: store one user
    */
    case ($method == 'POST' && $uri == '/api/users'):
        header('Content-Type: application/json');
        // with file_get_contents('php://input') we can get the request body
        // since it's in json we decode it with json_decode
        $requestBody = json_decode(file_get_contents('php://input'), true);
        $name = $requestBody['name'];
        if (empty($name)) {
            // there is no name in the request
            http_response_code(404);
            echo json_encode(['error' => 'Please add name of the user']);
        }
        // php gives it a new id automatically
        $users[] = $name;
        // conver the array to json and save the json in a file
        $data = json_encode($users, JSON_PRETTY_PRINT);
        file_put_contents($jsonFile, $data);
        echo json_encode(['message' => 'user added successfully']);
        break;
    /*
    * Path: PUT /api/users/{id}
    * Task: update one user
    */
    case ($method == 'PUT' && preg_match('/\/api\/users\/[1-9]/', $uri)):
        header('Content-Type: application/json');
        $id = basename($uri);
        if (!array_key_exists($id, $users)) {
            http_response_code(404);
            echo json_encode(['error' => 'user does not exist']);
            break;
        }
        $requestBody = json_decode(file_get_contents('php://input'), true);
        $name = $requestBody['name'];
        if (empty($name)) {
            http_response_code(404);
            echo json_encode(['error' => 'Please add name of the user']);
        }
        // update the name for that specific id and save the data to json file
        $users[$id] = $name;
        $data = json_encode($users, JSON_PRETTY_PRINT);
        file_put_contents($jsonFile, $data);
        echo json_encode(['message' => 'user updated successfully']);
        break;
    /*
    * Path: DELETE /api/users/{id}
    * Task: delete one user
    */
    case ($method == 'DELETE' && preg_match('/\/api\/users\/[1-9]/', $uri)):
        header('Content-Type: application/json');
        // get the id
        $id = basename($uri);
        if (empty($users[$id])) {
            http_response_code(404);
            echo json_encode(['error' => 'user does not exist']);
            break;
        }
        // check if there is only one user left don't delete it
        if (sizeof($users) == 1){
            http_response_code(404);
            echo json_encode(['error' => 'there is only one user left. you cannot delete it!']);
            break;
        }
        // remove that specific user from the users
        // and save the new users data to file
        unset($users[$id]);
        $data = json_encode($users, JSON_PRETTY_PRINT);
        file_put_contents($jsonFile, $data);
        echo json_encode(['message' => 'user deleted successfully']);
        break;
    /*
    * Path: ?
    * Task: this path doesn't match any of the defined paths
    *      throw an error
    */
    default:
        http_response_code(404);
        echo json_encode(['error' => "We cannot find what you're looking for."]);
        break;
}