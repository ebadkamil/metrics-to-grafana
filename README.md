# metrics and logs to Grafana and Graylog
  - Publish metrics to carbon server and visualize on Grafana
  - Publish logs to graylog.

Before publishing the metrics and logs, we need to run graylog, graphite and grafana server on
the local machine.

# Running Publisher, Graphite, Graylog and Grafana server using Docker

Use docker-compose and have it running in seconds.

        docker-compose up # in the root folder

Before running the above command, make sure to stop (if any) graphite, grafana, mongodb, elasticsearch
and graylog containers/services.

        docker stop $(docker ps -a -q)
        docker rm $(docker ps -aq)
        docker rmi $(docker images -q) # Not required to remove already existing images.
        sudo systemctl stop {service-name} # If any of the above services running as systemd

To check if all the servers are running

* open the graphite front-end dashboard
  - http://localhost/dashboard
* Open the graylog UI
  - http://127.0.0.1:9000
* Open Grafana web interface
  - http://localhost:3000

> **_NOTE:_** docker-compose up will start all the services including the publisher.
> If you intend to not launch metrics_to_grafana service do,

        docker-compose up --scale metric=0 # Exclude the metrics publisher

> If you wish to install metrics and log publisher as a standalone application follow the steps below.

# Installing the metrics publisher

`metrics_to_grafana`

Create virtual environment with Python 3.6 or later:

    git clone https://github.com/ebadkamil/metrics-to-grafana.git
    cd metrics-to-grafana
    python3 -m venev {env_name}

Activate virtual environment and install `metrics-to-grafana`:

    source {env_name}/bin/activate
    pip install .

Usage:

- Start consuming ESS flatbuffer messages from given topics

        start_load_publisher -g {grafana-carbon-address} -gl {graylog-logger-address} -l {log-level}
        grafana-carbon-address: for eg. "localhost"
        graylog-logger-address: for eg. "localhost:12201"
        log-level: for eg. debug, info, error, warn

# Configuring Graylog and Grafana.

Adding Graphite as a Data Source in Grafana |  Adding GELF TCP input in Graylog
:-------------------------:|:--------------------------------------------------:
![](./img/grafana_data_source.png)  |  ![](./img/graylog_input.png)

# Finally create appropriate dashboards in Graylog

![](./img/graylog_dashboard.png)