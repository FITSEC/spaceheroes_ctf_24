docker build -t lil .
docker run --name lil --rm -v /var/run/docker.sock:/var/run/docker.sock -p 5000:5000 lil

