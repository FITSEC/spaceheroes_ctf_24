docker build . -t build_arch
docker run --rm -p 5000:5000 -v "./:/root/a_riskv_maneuver/" -ti localhost/build_arch:latest

