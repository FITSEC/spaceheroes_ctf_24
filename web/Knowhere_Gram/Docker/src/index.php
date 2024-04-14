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
            padding-top: 100px; /* Add padding to top of body */
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

<div class="container-bg">
<div class="container text-center my-5">
    <h2 class="font-weight-light">Knowhere gram</h2>
    <div class="row mx-auto my-auto justify-content-center">
        <div id="recipeCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner" role="listbox">
                <div class="carousel-item active">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/rocket.webp" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/knowhere.avif" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/rocket-4.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/baby-groot-6.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/rocket-groot.jpg" class="img-fluid">
                            </div>
                            <div class="card-img-overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-img">
                                <img src="static/images/rocket-5.webp" class="img-fluid">
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

<div id="buttons" class="row justify-content-center">
        <div class="col-2">
            <a href="signup.php" class="btn btn-lg btn-black">Signup</a>
        </div>
        <div class="col-2">
            <a href="login.php" class="btn btn-lg btn-black">Login</a>
        </div>
    </div>

<script>

let items = document.querySelectorAll('.carousel .carousel-item')

items.forEach((el) => {
    const minPerSlide = 5
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
