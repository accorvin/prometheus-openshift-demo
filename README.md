# prometheus-openshift-demo

A demo of Prometheus running on openshift monitoring an application running
in the same openshift cluster

Credit to [1] for the source of much of this. I've adapted their source code
and examples to be more suited to my use case. The main adjustment is moving
the prometheus and prometheus alerts configurations to files for easier
maintenance in git.

# Setup

Perform the following to set up the demo environment. These instructions
assume you are familiar with the ```oc``` command and that you have already
logged into an openshift instance using the ```oc login``` command.

Note also that in the below commands there are several instances of:
```-n prometheus```
or
```-p NAMESPACE=prometheus```

Here, "prometheus" refers to the name of the project created in the initial
```oc new-project prometheus``` command. If a different project name is used,
the commands should be adjusted accordingly.

## Deploying prometheus

* Create an openshift project for the prometheus deployment

  ```oc new-project prometheus```

* Create a secret for the prometheus config and rules file

  ```oc create secret generic prometheus --from-file=prometheus.yml \
--from-file=alertmanager.yml -n prometheus```

* Create a secret for the prometheus alertmanager config
  ```oc create secret generic prometheus-alerts --from-file=alertmanager.yml \
-n prometheus```

* Deploy the prometheus stack to openshift using the openshift definition file
  ```oc process -f prometheus-openshift-template.yml -p NAMESPACE=prometheus | \
oc apply -f -```

* Once the pod deploys successfully, you should be able to view the prometheus
  web interface using the URL found by running
  ```oc get route prometheus -n prometheus```

## Deploying grafana

I like to use Grafana to view metrics from prometheus. These steps were taken
directly from [1] and repeated here for easy referencing.

* Create a new project for grafana
  ```oc new-project grafana```

* Deploy the grafana app
  ```oc new-app -f https://raw.githubusercontent.com/ConSol/\
springboot-monitoring-example/master/templates/grafana.yaml \
-p NAMESPACE=grafana```

* Add the ```view``` role to the grafana service account on the prometheus
  project
  ```oc policy add-role-to-user view system:serviceaccount:grafana:grafana-ocp \
-n prometheus```

## Configure grafana to access prometheus as a data source

* Navigate to the grafana service URL found using
  ```oc get route grafana-ocp -n grafana```

* Click the "Add data source" button

* Enter a name for the data source, for example: Prometheus-OCP

* For the data source type, select Prometheus

* For the URL, enter the endpoint specified in the "endpoints" key when running
  ```oc describe service prometheus -n prometheus```. Note that you will have to
  prepend the endpoint with "http://"

* Click the "Save & Test" button. You should see a message stating that the
  data source is working

[1] https://labs.consol.de/development/2018/01/19/openshift_application_monitoring.html
