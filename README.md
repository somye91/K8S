# K8S

This is built and tested with minikube

Step 1:
`minikube start`


Step 2: 
Navigate to the directory where your Dockerfile, requirements.txt and scratch.py is. And build the docker image sampleapp
`docker build -t sampleapp:latest . `

Step 3:
Create kubernetes objects using the K8S yaml fies
`kubectl apply -f deployment.yaml`
This will create the micro-service from the sampleapp docker image that we created in Step2. 4 replicas would  always be created and maintained by kubernetes. 

`kubectl apply -f service.yaml`
This will create a service that ties with the micro-service that we just created. Other kubernetes pods can access our micro-service using this service we just created hello-python-service:5000

Step 4:
Create the cronjob in kubernetes that writes the HTTP status returned by the micro-service o a log file
`kubectl apply -f cron.yaml`
This will create a cronjob in kubernetes using a lightweight alpine image and is scheduled to run evey 2 mins. It checks the HTTP response of the micro-service from Step2 and logs http500 to a log file which is mounted to the actual host using volumes

If you are using minikube, then you have to do an extra step before Step 4
`minikube mount dir/on/host:dir/on/minikubeVM`



<H3>How to reduce the attack surface of the docker images even more </h3>
Using distroless images would be the way to go.
Since i used python, i could make use of Google's distroless images around Python3
Reference: https://github.com/GoogleContainerTools/distroless/tree/main/examples/python3
<p>This image is bare minimal, we could package our app to this image which would result in an even lesser attack surface

I could even use the same python distroless container to create the service container that checks the health of the micro-service. Then i do no need to use the curl command anymore and everything could be done in python.
It would be an interesting set up since the distroless image from Google does not even have a shell to begin with. A really really small attack surface

</p>

<H3>Improving the design to generate an alert based on error ratio per minute </h3>
<p>
 The microservice itself should log the following metrics
<ul>
  <li>The number of HTTP requests that result in 2XX or 5XX responses</li>
  <li>Latency of HTTP 2XX responses </li>
 The problem with this is that monitoring traffic is drectly proportional to the user traffic. We woud like to create an independent monitoring system that does not rely on actual user traffic.
And open source monitoring tools such as Prometheus can also be deployed within the same kubernetes cluster that can monitor the microservice(s) and represent the various KPIs graphically. There are a bunch of aggregations ready to be used within Prometheus that could trigger an alert based on error ratio per time, or latency per time etc.  
</ul>
</p>
