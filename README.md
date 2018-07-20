# prometheus-openshift-demo

A demo of Prometheus running on openshift monitoring a Flask application
running on the same openshift cluster

# OpenShift Environment

You should be able to perform the following steps from a clean minishift
environment. The following show the openshift versions that I have tested
this with:

```
Alexs-MBP:prometheus-openshift-demo acorvin$ minishift version
minishift v1.17.0+f974f0c

Alexs-MBP:prometheus-openshift-demo acorvin$ oc version
oc v3.9.0+191fece
kubernetes v1.9.1+a0ce1bc657
features: Basic-Auth

Server https://192.168.64.3:8443
openshift v3.9.0+0e3d24c-14
kubernetes v1.9.1+a0ce1bc657
```

Note that I had to provision minishift with more than default RAM using the
following command:

```minishift start --memory 4GB```

Perform the following to set up the demo environment. These instructions
assume you are familiar with the ```oc``` command and that you have already
logged into an openshift instance using the ```oc login``` command.

# Deploy Prometheus

Create an openshift project for the prometheus deployment

```
oc new-project prometheus --display-name="Prometheus Server"
```

Deploy the prometheus stack to openshift using the openshift template file

```
oc process -f prometheus.yaml | oc apply -f -
```

Once the pod deploys successfully, you should be able to view the prometheus
web interface using the URL found by running

```
oc get route prometheus
```

# Deploy the demo application

This repo contains a sample Flask application for generating metrics in
prometheus. Perform the following to set up this application.

Create a new project for the demo application:

```
oc new-project demoapplication
```

Deploy the demo application using the openshift template:

```
oc process -f demoapplication/demoapplication.yaml | oc apply -f -
```

You should now be able to access the demo application using the URL returned
by:

```
oc get route demoapplication
```

When you access the index/home page of the demo application, you should
see the words "Hello, world!". When you access the ```/metrics/``` page
of the demo application you'll see some prometheus metrics printed out.
You should see that the ```requests_count``` counter increments every time
you access the home page. (Note that there is a delay due to the frequency
at which the prometheus server queries for metrics).

## How Prometheus knows to pull metrics for the demoapplication

The important part here is that the demoapplication service in OpenShift
has the annotation ```prometheus.io/scrape: "true"``` defined in its
metadata (Line 50 in demoapplication/demoapplication.yaml). The Prometheus
server is configured to look for this annotation. At line 191 in
prometheus.yaml we tell the prometheus to query any services with this
endpoint for metrics using the /metrics/ URL.

## Some notes on the Flask changes

The following are the important bits for how the Flask demoapp was set up to
provide metrics:

  * Make sure the prometheus_client python package is installed

  * Add the import ```from prometheus_client import generate_latest, Counter```
    to your Flask app. Note that the demoapplication is a very simple app
    with not very realistic structure (it's just one python file). I'm not
    sure yet how to structure the imports in a more production-ready app.

  * Initialize a counter:
    ```requests_count = Counter('requests_count', 'The number of requests')```
    Note that there are other metric types supported by Prometheus, a counter
    is just the simple example I chose to start with. Support metrics are
    described [here][1].

  * Add a call to increment the counter somewhere by adding
    ```requests_count.inc()```

  * Add a ```/metrics/``` route to the flask app that returns
    ```Response(generate_latest())```

[1]: https://github.com/prometheus/client_python
