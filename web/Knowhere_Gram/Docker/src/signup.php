<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $username = $_POST['username'];
    $password = hash('sha256', ($_POST['password'])); // hashing the password
    
    // Check if username already exists
    $db = new SQLite3('users.db'); // Assuming SQLite database
    $stmt = $db->prepare('SELECT * FROM users WHERE username = :username');
    $stmt->bindValue(':username', $username);
    $result = $stmt->execute();
    
    if ($result->fetchArray(SQLITE3_ASSOC)) {
        // Username already exists
        echo "Username already exists. Please choose a different username.";
    } else {
        // Save to database
        $stmt = $db->prepare('INSERT INTO users (email, username, password, timestamp) VALUES (:email, :username, :password, :timestamp)');
        $stmt->bindValue(':email', $email);
        $stmt->bindValue(':username', $username);
        $stmt->bindValue(':password', $password);
        $stmt->bindValue(':timestamp', time());
        $stmt->execute();
        
        echo "User signed up successfully!";
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

    </style>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</head>
<body>
    
<div class="container-fluid bg-black" style="padding-top: 100px; padding-bottom: 250px;">
    <div class="row justify-content-center align-items-center">
        <div class="col-md-6">
            <div class="text-center mb-5" style="color: #fff;">
                <h2 class="heading-section">Login</h2>
            </div>
            <div class="login-wrap p-4 p-md-5">
                <h3 class="mb-4"></h3>
                <form action="" class="signup-form" method="post">
                    <div class="form-group mb-3">
                        <label class="label" for="email">email</label>
                        <input type="text" class="form-control" id="email" name="email" placeholder="email" required>
                    </div>
                    <div class="form-group mb-3">
                        <label class="label" for="username">Username</label>
                        <input type="text" class="form-control" id="username" name="username" placeholder="Username" required>
                    </div>
                    <div class="form-group mb-3">
                        <label class="label" for="password">Password</label>
                        <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
                    </div>
                    <div class="form-group mb-4">
                        <button type="submit" class="btn btn-lg btn-block btn-black rounded submit px-3" style="color: #fff;" >Sign Up</button>
                    </div>
                    <div class="form-group d-md-flex justify-content-between">
                        <div class="w-50 text-left">
                        </div>
                        <div class="w-50 text-right">
                            <p class="text-center" style="color: #fff;">Already Signed Up? <a href="login.php" class="text-white">Login</a></p>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="col">
            
                <img src="static/images/baby-groot-3.jpg" alt="Mountains" style="width:70%; height:800px;">
            </div>
        </div>
    </div>
</div>

</body>
</html>

