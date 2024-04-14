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
    
    .card {
    background-color: #000; /* Black background */
     /* Optional: Add padding for spacing */
}


.btn-black {
    background-color: #222; /* Darker black for buttons */
    color: #fff;
}
    
@media (max-width: 967px) {
    .carousel-inner .carousel-item > div {
        display: none;
    }
    .carousel-inner .carousel-item > div:first-child {
        display: block;
    }
}

.carousel-inner .carousel-item.active,
.carousel-inner .carousel-item-next,
.carousel-inner .carousel-item-prev {
    display: flex;
}

/* medium and up screens */
@media (min-width: 968px) {
    
    .carousel-inner .carousel-item-end.active,
    .carousel-inner .carousel-item-next {
      transform: translateX(25%);
    }
    
    .carousel-inner .carousel-item-start.active, 
    .carousel-inner .carousel-item-prev {
      transform: translateX(-25%);
    }
}

.carousel-inner .carousel-item-end,
.carousel-inner .carousel-item-start { 
  transform: translateX(0);
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

  <div class="container mt-5">

  <h1>Home Page</h1>
  <p id="welcomeMessage">Loading...</p>
  
  </div>  
<script src="script.js" defer></script> 
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

<div class="container-bg">
<div class="container text-bottom my-5">
    <h1 class="font-weight-light" style="color: #000;">|</h1>   
    <h1 class="font-weight-light" style="color: #000;">|</h1>
    <h1 class="font-weight-light" style="color: #000;">|</h1>
    <div class="row my-auto justify-content-center">
        <div id="recipeCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner" role="listbox">
                <div class="carousel-item active">
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/rocket-2.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/baby-groot-4.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/G-vol2-2.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/G-vol3.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/space-dog.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/rocket.webp" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
            </div>
           
        </div>
    </div>
    
</div>

</div>

<script>

let items = document.querySelectorAll('.carousel .carousel-item')

items.forEach((el) => {
    const minPerSlide = 2
    let next = el.nextElementSibling
    for (var i=1; i<minPerSlide; i++) {
        if (!next) {
            // wrap carousel by using first child
        	next = items[0]
      	}
        let cloneChild = next.cloneNode(true)
        el.appendChild(cloneChild.children[0])
        next = next.nextElementSibling
    }
})

</script>
 
</body>
</html>

