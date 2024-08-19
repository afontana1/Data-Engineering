# Author: Vinicio De Sola (username: penpen86)
# My annotations, Assignment 5.


## First, I'm moving the docker-compose.yml from Course Content
   282  cp ../course-content/05-Storing-Data-II/example-1-docker-compose.yml docker-compose.yml

## Next, I'm editing it using vi
   288  vi docker-compose.yml 

## I spin the cluster, check the logs
   293  docker-compose up -d
   294  docker-compose ps
   295  docker-compose logs

## Run a jupyter notebook in the mids container
   301  docker-compose exec mids jupyter notebook --no-browser --port 8080 --ip 0.0.0.0 --allow-root
   
## Take down the cluster
   303  docker-compose down
   
## Bonus: open a notebook directly from docker-compose
   302  vi docker-compose.yml
   315  docker-compose up -d
   316  docker-compose logs mids
   318  docker-compose down
   
## Extras: download trips.csv and run redis from the cluster in notebook
   317  vi docker-compose.yml
   322  cd ~/w205
   323  curl -L -o trips.csv https://goo.gl/QvHLKe
   327  docker-compose up -d
   328  docker-compose logs mids
   329  docker-compose down 
   330  history > penpen86-history.txt
