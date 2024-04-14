<?php
//session_destroy();
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = hash('sha256', ($_POST['password'])); 
    
    
    $db = new SQLite3('users.db'); 
    $stmt = $db->prepare('SELECT id, username FROM users WHERE username = :username AND password = :password');
    $stmt->bindValue(':username', $username);
    $stmt->bindValue(':password', $password);
    $result = $stmt->execute()->fetchArray(SQLITE3_ASSOC);
    
    if ($result) {
    
    $id = $result['id']; 
    $token = bin2hex(random_bytes(16)); 
 
    
    $db = new SQLite3('users.db'); 
    $stmt = $db->prepare('INSERT INTO login_sessions (user_id, token) VALUES (:user_id, :token)');
    $stmt->bindValue(':user_id', $id);
    $stmt->bindValue(':token', $token);
    $stmt->execute();
 
    
    header("Location: home.php?id=" . $id . "&token=" . $token);
    exit();
    } else {
        echo "<script>alert('Invalid username or password')</script>" ;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            
        }
        .bg-black {
            background-color: #000;
        }
        .text-white {
            color: #fff;
        }
        .label {
        color: #fff; /* Set the text color to white */
    }
        .btn-black {
            background-color: #222;
            color: #fff;
            border-color: #222;
        }
        .btn-black:hover {
            background-color: #444;
            border-color: #444;
        }
        .img-container {
            height: 500px; /* Adjust the desired height for the image container */
            background-image: url('static/images/rocket.webp');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</head>
<body>
    
<div class="container-fluid bg-black" style="padding-top: 200px; padding-bottom: 250px;">
    <div class="row justify-content-center align-items-center">
        <div class="col-md-6">
            <div class="text-center mb-5" style="color: #fff;">
                <h2 class="heading-section">Login</h2>
            </div>
            <div class="login-wrap p-4 p-md-5">
                <h3 class="mb-4"></h3>
                <form action="" class="login-form" method="post">
                    <div class="form-group mb-3">
                        <label class="label" for="username">Username</label>
                        <input type="text" class="form-control" id="username" name="username" placeholder="Username" required>
                    </div>
                    <div class="form-group mb-3">
                        <label class="label" for="password">Password</label>
                        <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
                    </div>
                    <div class="form-group mb-4">
                        <button type="submit" class="btn btn-lg btn-block btn-black rounded submit px-3" style="color: #fff;" >Login</button>
                    </div>
                    <div class="form-group d-md-flex justify-content-between">
                        <div class="w-50 text-left">
                        </div>
                        <div class="w-50 text-right">
                            <p class="text-center" style="color: #fff;">Not a member? <a href="signup.php" class="text-white">Sign Up</a></p>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="col-md-6">
            <div class="img-container">
                <!-- Background image will be displayed here -->
            </div>
        </div>
    </div>
</div>

</body>
</html>

