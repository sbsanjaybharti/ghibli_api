# ghibli API
Flask application to serve data from ghibli api

#### Description:
1. Memcache server used to store cache.
2. If cache does not exist then it will create the cache and serve the data
3. If cache exist then check if cache is not older than one min then get the data from cache and serve the data
4. If cache exist but older than one minute then compare the data and check new release on ghibhi and if we find any new release then append the data in existing cache and serve the data

### Requirement:
* Python
* Flask
* Memcache
* docker
### List of content
1. Architecture
2. Running url on docker
3. Memcache container to manage cache
4. Unit test with 44 test cases
5. PEP8 with pylint

### Architecture
#### System Architecture:
![](system_architecture-L1-System_Archtecture.png)
#### Solution Architecture:
![](system_architecture-L2-Application_flow.png)
<br/>You can open the architecture design in draw.io also by
opening https:draw.io and select the file system_architecture.drawio

#### Folder Structure:
    --ghibli(main application)
      --src
        --__init__.py
        --config.py
        --ghibhi.py
        --service.py
      --templates
        --index.html
      --test
        --__init__.py
        --base.py
        --test_cache.py
        --test_ghibhi.py
        --test_movie.py
        --test_people.py
        --test_servive.py
      --__init__.py
      --app.ini
      --docker-local-entrypoint.sh
      --local.Dockerfile
      --requirement.txt
      --run.py(main file to run application)
    --nginx
    --docker-compose.yml
    --traefik.toml(to monitor the trafic with list of url)
#### Step-1
1. Install Docker 
2. git clone https://github.com/sbsanjaybharti/ghibli_api.git
3. I am assuming Docker is already install in your system if not then follow this link https://docs.docker.com/get-docker 
3. Open the terminal in main folder and run the command<br/>
```ubuntu
docker-compose build
docker-compose up
```
#### Step-2
1. Create cache on server by command line (Optional), first command will take you in the container and second command will create cache.
```python 
docker-compose exec ghibli /bin/bash 
python run.py create_cache
``` 
2. open the link http://nginx.localhost/movies.
3. To run the test cases open new terminal in same folder and run the command, first command will take you in the container and second command to run the test.
```python 
docker-compose exec ghibli /bin/bash 
python run.py test
``` 
4. To test PEP8 status
```python 
docker-compose exec ghibli /bin/bash 
python -m pylint <filename>
``` 
first command will take you in the container and second command to run the pylint.
replace <filename> with actual file name eg. run.py, src/service.py and so on

 
##### Advantage:
1. First time it will take time to load all the movie in cache
2. After that it will take get the data from cache so it will be faster.
3. Optimized code is written 
4. Archtecture is best for non concurent user.
5. Minimum hit to Ghibli API
6. Initial cache can be creat by command line also if data is very high.

