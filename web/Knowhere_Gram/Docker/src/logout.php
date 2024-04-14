<?php


if (isset($_GET['id']) && isset($_GET['token'])) {

    $id = $_GET['id'];
    $token = $_GET['token'];


    $db = new SQLite3('users.db'); 

    $stmt = $db->prepare('DELETE FROM login_sessions WHERE user_id = :id AND token = :token');
    $stmt->bindValue(':id', $id);
    $stmt->bindValue(':token', $token);


    $result = $stmt->execute();
   
    if ($result) {
         echo "You have successfully logged out!";
        //header("Location: index.php");
        //exit(); 
    } else {

        echo "Error deleting token and user ID from database.";
    }
} else {

    echo "ID and token parameters are required.";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowhere Gram</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>


    <!-- Custom styles -->
    <style>
    
body {
            background-color: #000;
            color: #fff;
            padding-top:; /* Add padding to top of body */
        } 

.btn-black {
    background-color: #222; /* Darker black for buttons */
    color: #fff;
}

.center{
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;


}

 </style>
</head>

<body>
          
<img src="static/images/baby-groot-7.jpg" alt="Mountains" class="center">


<div id="buttons" class="row justify-content-center">
        <div class="col-2">
            <a href="signup.php" class="btn btn-lg btn-black">Signup</a>
        </div>
        <div class="col-1">
            <a href="login.php" class="btn btn-lg btn-black">Login</a>
        </div>
    </div>

</body>
</html>
