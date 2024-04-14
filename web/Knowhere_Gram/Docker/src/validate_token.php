<?php
header('Content-Type: application/json');

if (isset($_POST['id']) && isset($_POST['token'])) {
    $id = $_POST['id'];
    $token = $_POST['token'];
    $db = new SQLite3('users.db');
    $stmt = $db->prepare('SELECT user_id, token FROM login_sessions WHERE token = :token');
    if (!$stmt) {
        echo json_encode(['error' => 'Database error: ' . $db->lastErrorMsg()]);
        exit();
    }
    $stmt->bindValue(':token', $token);
    $result = $stmt->execute();
    if ($result) {
        $row = $result->fetchArray(SQLITE3_ASSOC);
        $storedUserId = $row['user_id'];
        $storedToken = $row['token'];
        if ($storedUserId == $id && $storedToken == $token) {
            echo json_encode(['valid' => true]); 
        } else {
            echo json_encode(['valid' => false]); 
        }
    } else {
        echo json_encode(['error' => 'Database error: Unable to execute query']);
    }
} else {
    echo json_encode(['error' => 'Missing id or token on validate.php']);
}
?>

