<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
error_log("function got called");
$target_dir = "uploads/";
$target_name = bin2hex(random_bytes(8)) . ($_FILES["fileToUpload"]["name"]);
$target_file = $target_dir . $target_name;
$uploadOk = 1;
$imageFileType = ($_FILES["fileToUpload"]["type"]);

if (file_exists($target_file)) {
  echo "<script>alert('Sorry, file already exists.')</script>";
  $uploadOk = 0;
}

// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
  echo "<script>alert('Sorry, your file is too large.')</script>";
  $uploadOk = 0;
}

// Allow certain file formats
if($imageFileType != "image/jpg" && $imageFileType != "image/png" && $imageFileType != "image/jpeg" && $imageFileType != "image/gif" ) {
  echo "<script>alert('Sorry, only JPG, JPEG, PNG & GIF files are allowed.')</script>";
  $uploadOk = 0;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
  echo "<script>alert('Sorry, your file was not uploaded.')</script>";
// if everything is ok, try to upload file
} else {
   if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    echo "<script>alert('The file ". htmlspecialchars( $target_name) . " has been uploaded.')</script>";
   } else {
    echo "Sorry, there was an error uploading your file.";
   }
 }

}

if (isset($_GET['id']) && isset($_GET['token'])) {
    $id = $_GET['id'];
    $token = $_GET['token'];
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
            
    
                $db = new SQLite3('users.db');
    
                $stmt = $db->prepare('SELECT username FROM users WHERE id = :id');
                $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    
                $result = $stmt->execute();
    
                if ($result) {
                    $row = $result->fetchArray(SQLITE3_ASSOC);
                    $retrivedUsername = $row['username'];
                    //error_log("retrivedUsername:" . $retrivedUsername);
                    if ($retrivedUsername === "admin") {
                        echo"<!DOCTYPE html>";
			echo"<html>";
			echo"<head>";
			echo"    <style>";
			echo"        body {";
			echo"            background-color: #000;";
			echo"            color: #fff;";
			echo"            font-family: Arial, sans-serif;";
			echo"        }";
			echo"         form{";
			echo"		  position: fixed;";
			echo"		  top:40%;"; 
			echo"		  width:250px;";
			echo              "left:40%;";
			echo"		}";
			echo"    </style>";
			echo"</head>";
			echo"<body>";
			echo'<form id="form" align="center" action="" method="post" enctype="multipart/form-data">';
			echo"Select image to upload:";
			echo'<input type="file" name="fileToUpload" id="fileToUpload">';
			echo'<input type="submit" value="Upload Image" name="submit">';
			echo"</form>";
			echo"</body>";
			echo"</html>";

                        
                    } else {
                        
                        echo "<script>alert('You are not an admin')</script>" ;   
                        
                        
                    }
        
                }  
       
        } else {
                echo json_encode(['valid' => false]);
                header("Location: login.php");  
        }
    } else {
        echo json_encode(['error' => 'Database error: Unable to execute query']);
    }

} 


?>

<!DOCTYPE html>
<html>

<head>
  <title>Home Page</title>
  
  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #000;
      color: #fff;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }

    /* Adjust navbar color */
    .navbar {
      background-color: #000;
    }

    /* Adjust link color */
    .navbar-dark .navbar-nav .nav-link {
      color: #fff;
    }
  </style>
</head>
<body>
  
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
      
      <a class="navbar-brand" href="home.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Knowhere-Gram</a>

      
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link" href="home.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="profile.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Profile</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="image.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Image</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="upload.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Upload</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="logout.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Logout</a>
        </li>
      </ul>
    </div>
  </nav>

  <div class="container mt-5">

  <h1>Home Page</h1>
  <p id="welcomeMessage">Loading...</p>
  
  </div>
  
  <script src="script.js" defer></script> 
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  
  
</body>
</html>

