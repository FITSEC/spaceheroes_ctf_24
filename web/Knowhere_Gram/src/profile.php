<?php
if (isset($_GET['token']) && isset($_GET['id'])) {
  $token = $_GET['token'];
  $id = $_GET['id'];

} else {
  // Handle case where id is not provided (optional: redirect or error message)
  header("Location: login.php"); 
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/js/all.min.js" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css">
    

    <!-- Custom styles -->
<style>


* {
    margin: 0;
    padding: 0
}

 body {
      background-color: #000;
    }
    
    /* Adjust navbar color */
    .navbar {
      background-color: #000;
    }

    /* Adjust link color */
    .navbar-dark .navbar-nav .nav-link {
      color: #fff;
    }
    

.card {
    width: 430px;
    background-color: #efefef;
    border: none;
    cursor: pointer;
    transition: all 0.5s;
}

.image img {
    transition: all 0.5s
}

.card:hover .image img {
    transform: scale(1.3)
}

.btn {
    height: 140px;
    width: 140px;
    border-radius: 50%
}

.name {
    font-size: 30px;
    font-weight: bold
}

.idd {
    font-size: 20px;
    font-weight: 600
}

.idd1 {
    font-size: 22px
}

.number {
    font-size: 22px;
    font-weight: bold
}

.follow {
    font-size: 12px;
    font-weight: 500;
    color: #444444
}

.btn1 {
    height: 40px;
    width: 150px;
    border: none;
    background-color: #000;
    color: #aeaeae;
    font-size: 15px
}

.text span {
    font-size: 18px;
    color: #545454;
    font-weight: 500
}

.icons i {
    font-size: 20px;
}

hr .new1 {
    border: 1px solid
}

.join {
    font-size: 14px;
    color: #a0a0a0;
    font-weight: bold
}

.date {
    background-color: #ccc
}

.btns{
border: transparent;
margin: 5px;

}

.ship {
    font-size: 20px;
    font-weight: bold
}
    </style>
</head>

<body>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
      
      <a class="navbar-brand" href="home.php?id=<?php echo $id; ?>&token=<?php echo $token; ?>">Knowhere-Gram</a>

      
      <ul class="navbar-nav ms-auto">
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

<?php
    $db = new SQLite3('users.db');
    
    $stmt = $db->prepare('SELECT username FROM users WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    
    $result = $stmt->execute();
    
    if ($result) {
        $row = $result->fetchArray(SQLITE3_ASSOC);
        $retrivedUsername = $row['username'];
        //error_log("retrivedUsername:" . $retrivedUsername);
            if ($retrivedUsername === "admin") {


echo '
<div class="container mt-5 mb-5 p-5 d-flex justify-content-center"> 
  <div class="card p-4">
    <div class=" image d-flex flex-column justify-content-center align-items-center">
      <button class="btn"> <img src="static/images/rocket-profile.jpg" height="160" width="125" />
       </button> 
 
      <span class="name mt-5">Rocket Raccoon</span> 
      <span class="idd1">Alias: Ranger Rocket</span>
      <span class="idd">admin</span> 
      <div class="d-flex flex-row justify-content-center align-items-center gap-2">
         
          
            </div> <div class="d-flex flex-row justify-content-center align-items-center mt-3">
              <span class="number"> <span class="follow"></span>
          </span> 
           </div> 
               <div class="text mt-2"> 
                 <span><h4>Guardian of the Galaxy</h4><br>Skilled marksman and hand-to-hand combatant<br>Master tactician and field commander<br>Accomplished starship aviator<br>Genius-level intellect<br>Last but not least:</span>
                 <span><h5 class="ship">"Captain of all the ships"</h5>
               </div>
               <div class="gap-3 mt-3 icons d-flex flex-row justify-content-center align-items-center">
              <button class="btns" id="twitter-id"><span class="twitter"><i class="fab fa-twitter"></i></span></button>
              <button class="btns" id="fb-id"><span class="facebook"><i class="fab fa-facebook-f"></i></span></button>
              <button class="btns" id="insta-id"><span class="instagram"><i class="fab fa-instagram"></i></span></button>
                 
               </div> 
            </div>
          </div>
</div>

<script>
let btnt = document.getElementById("twitter-id");
let btnf = document.getElementById("fb-id");
let btni = document.getElementById("insta-id");


btnt.addEventListener("click", myFunction);
btnf.addEventListener("click", myFunction);
btni.addEventListener("click", myFunction);



function myFunction(){
    alert("We don\'t have social media here!!");
}
</script>  ';

     }
  
	else{
	echo "<div class='container mt-5 mb-5 p-5 d-flex justify-content-center' style='height:700px; width:450px;'>";
	echo '  <div class="card p-4">';
	echo '    <div class=" image d-flex flex-column justify-content-center align-items-center">';
	echo '      <button class="btn"> <span class="user"><i class="fas fa-user-circle" style="font-size:120px"></i></span>';
	echo '       </button> ';
	echo '      <span class="name mt-2">'; echo $retrivedUsername;
	echo '      </span> ';
	echo '      <span class="idd1"></span>';
	echo '      <span class="idd">User</span> ';
	echo '      <span class="idd">No Information found!!</span> ';

}

}

?>

</body>
</html>
