# Cronitor RUM Relay

Relay enables [Cronitor RUM](https://cronitor.io/docs/real-user-monitoring) customers to process personal data on a server they control while leveraging our platform for data storage and analytics.

This server becomes the first point of contact for your visitor's data and strips out IP addresses before they even reach our servers.

## Use Cases

Relay is meant to support our customers in the following ways

- Facilitate privacy and security compliance by processing personal data in a server you control.
- Reduce exposure of user IP addresses to third parties.
- Retain the ability to perform geo lookups and assign session IDs for RUM data.

## Basic deployment

The relay server is docker-based, making it easy to deploy and run.

1. Install Docker on your server.
2. Pull the image using the following command:
    ```
    docker pull ghcr.io/cronitorio/cronitor-rum-relay:latest
    ```
3. Run the RUM Relay Server using the following command, replacing the placeholders with your configuration values:
    ```
    docker run -it -p 80:8000 ghcr.io/cronitorio/cronitor-rum-relay:latest
    ```

Assuming your server is accessible at `https://rum.example.com`, you can now point your Cronitor RUM installation to use this server by setting the `ingestionHost` option accordingly:

```html
<script>
     window.cronitor = window.cronitor || function() { (window.cronitor.q = window.cronitor.q || []).push(arguments); };
     cronitor('config', {
         clientKey: 'YOUR_CLIENT_KEY',
         debug: false,
         ingestionHost: 'https://rum.example.com',  // <-- HERE
     });
 </script>
```

## Deployment with geolocation

If you want to use the geolocation feature, you will need to download the [MaxMind GeoIP City database](https://dev.maxmind.com/geoip/geoip2/geolite2/) and mount it as a volume when running the container:

1. Download the GeoIP City database file from [MaxMind](https://dev.maxmind.com/geoip/geoip2/geolite2/) based on your licensing requirements.
2. Unzip it to a local directory, and start the container with its path mounted:
  ```
  docker run -it \
     -p 80:8000 \
     -e SECRET_SALT=<your-secret> \
     -e GEO_IP_CITY_DATABASE=/opt/GeoLite2-City.mmdb \
     -v ${PWD}/GeoLite2-City.mmdb:/opt/GeoLite2-City.mmdb \
     ghcr.io/cronitorio/cronitor-rum-relay:latest
  ```

## Deployment without Docker

You can run the relay server without Docker if you prefer. To do so, you will need to install [Python 3.11+](https://www.python.org/downloads/) with [pip](https://pip.pypa.io/en/stable/installing/).

1. Clone the repository:
    ```
    git clone https://github.com/cronitorio/cronitor-rum-relay
    cd cronitor-rum-relay
    ```
2. Set up the virtual env and install the dependencies:
    ```
    bin/install.sh
    ```
3. Start the server:
    ```
    bin/start.sh
    ```

By default, it will be listening on port `8000`. You can change this by setting the `PORT` environment variable.

## Production recommendations

We recommend the following when deploying the relay server in production

- Use a reverse proxy such as [NGINX](https://www.nginx.com/) to terminate TLS and proxy requests to the relay server.
- Set the `SECRET_SALT` environment variable to a secure random string and keep it secret.
- Regularly update the GeoIP City database file to ensure accurate geolocation data.

If you run the server as a regular system process instead of using the docker-based deploy, we recommend doing so with a process manager such as [supervisord](http://supervisord.org/) to ensure the server is kept up-and-running.

## Available Settings

The following environment variables are available to customize the behavior of the relay server:

- **SECRET_SALT**: The secret salt used to generate the session ID. Defaults to a secure random string that changes on server start.
- **DRY_MODE**: Set to true to enable dry mode, which logs the processed events without recording them in Cronitor. Default is `false`.
- **UPSTREAM_HOST**: The Cronitor RUM hostname to send events to. Defaults to `https://rum.cronitor.io`.
- **GEO_IP_CITY_DATABASE**: The path to the MaxMind GeoIP City database file. For example `/opt/GeoLite2-City.mmdb`.

## Security
If you discover any issue regarding security, please disclose the information responsibly by emailing us at support@cronitor.io. Do NOT create a Issue on the GitHub repo.

## Contributing

Please check for any existing issues before opening a new Issue. If you'd like to work on something, please open a new Issue describing what you'd like to do before submitting a Pull Request.

## License

See [LICENSE](https://github.com/cronitorio/cronitor-rum-relay/blob/master/LICENSE).
