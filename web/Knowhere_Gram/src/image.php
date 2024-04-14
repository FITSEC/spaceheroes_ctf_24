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


* {
  box-sizing: border-box;
}

.row {
  display: flex;
}

/* Create three equal columns that sits next to each other */
.column {
  flex: 33.33%;
  padding: 5px;
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

  <h1>Images</h1>
  
  </div>  

<div class="row">
  <div class="column">
    <img src="static/images/baby-groot-1.jpg" alt="Snow" style="width:100%">
  </div>
  <div class="column">
    <img src="static/images/baby-groot-2.jpg" alt="Forest" style="width:100%">
  </div>
  <div class="column">
    <img src="static/images/baby-groot-6.jpg" alt="Mountains" style="width:100%">
  </div>
</div> 

<div>
<h1 style="color:#000;">|</h1>
<h1 style="color:#000;">|</h1>
<h1 style="color:#000;">|</h1>
</div>

<div class="row">
  <div class="column">
    <img src="static/images/G-vol1.jpg" alt="Snow" style="width:100%">
  </div>
  <div class="column">
    <img src="static/images/G-vol1-1.jpg" alt="Forest" style="width:100%">
  </div>
  <div class="column">
    <img src="static/images/G-vol2.jpg" alt="Mountains" style="width:100%">
  </div>
</div> 
    
<div>
<h1 style="color:#000;">|</h1>
<h1 style="color:#000;">|</h1>
<h1 style="color:#000;">|</h1>
</div> 

<div class="row">
  <div class="column">
    <img src="static/images/rocket-and-space-dog.jpg" alt="Snow" style="width:100%">
  </div>
  <div class="column">
    <img src="static/images/rocket-1.jpg" alt="Forest" style="width:100%">
  </div>
  <div class="column">
    <img src="static/images/rocket-3.jpg" alt="Mountains" style="width:100%">
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

