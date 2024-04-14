<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id = $_POST['id'];
    $db = new SQLite3('users.db');
    
    $stmt = $db->prepare('SELECT * FROM users WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    
    $results = $stmt->execute();
    $data = [];
    while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
        $data[] = $row;
    }

    $db->close();
    header('Content-Type: application/json');
    echo json_encode($data);
} else {
    echo json_encode(['error' => 'ID parameter is missing']);
}
?>

