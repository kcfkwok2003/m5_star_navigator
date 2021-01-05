docker run -it -v d:/kcf_test/docker/mpy:/mpy mattyt/esp32-micropython-dev

FROM mattyt/esp32-micropython-dev
export ESPIDF=/mpy/esp-idf
apt-get update
apt-get install python3
apt-get install --fix-missing python3-pip
python3 -m pip install pyparsing==2.3.1

docker build .
docker tag <id> kcfkwok/esp32-micropython-dev

docker run -it -v d:/kcf_test/docker/mpy:/mpy mattyt/esp32-micropython-dev

