# metrics-to-grafana
  - Publish metrics to carbon server and visualize on Grafana

Before publishing the metrics, we need to install graphite and grafana server on
the local machine.

# Installing and running graphite server

Try Graphite in Docker and have it running in seconds.

        docker run -d \
        --name graphite \
        --restart=always \
        -p 80:80 \
        -p 2003-2004:2003-2004 \
        -p 2023-2024:2023-2024 \
        -p 8125:8125/udp \
        -p 8126:8126 \
        graphiteapp/graphite-statsd

To check if server is running open the graphite front-end dashboard

* http://localhost/dashboard


# Install and running Grafana service:
### Ubuntu 20.04

* Add the Grafana APT repositories to your server

        sudo apt-get install -y apt-transport-https
        sudo apt-get install -y software-properties-common wget

* Add the GPG key to the trusted keys

        wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

* Add the trusted Grafana repositories

        echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

* Install

        sudo apt-get update
        sudo apt-get install grafana

* Start the grafana-server using systemctl

        sudo systemctl start grafana-server
        sudo systemctl status grafana-server

* Launch grafana web interface

    - http://localhost:3000

        - By default, the login and password for Grafana is “admin”.
        - Change password when prompted.

> For more information check https://grafana.com/docs/grafana/latest/installation/debian/
### macOS

Install with Homebrew

    brew update
    brew install grafana

The brew page downloads and untars the files into /usr/local/Cellar/grafana/version.

Start Grafana using the command:

    brew services start grafana

> For more information check https://grafana.com/docs/grafana/latest/installation/mac/
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

        start_load_publisher -g {grafana-carbon-address} -l {log-level}
        grafana-carbon-address: for eg. "localhost"
        log-level: for eg. debug, info, error, warn