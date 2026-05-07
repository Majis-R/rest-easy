#!/bin/bash

domains=("bubly.duckdns.org")
rsa_key_size=4096
email="${SSL_EMAIL}"
staging=0 # Set to 1 if you're testing your setup to avoid hitting request limits

if ! [ -x "$(command -v docker-compose)" ]; then
    echo 'Error: docker-compose is not installed.' >&2
    exit 1
fi

echo "### Cleaning up old containers to prevent ContainerConfig errors ..."
docker-compose down --remove-orphans || true
# Kill and remove everything just to be safe from the bug
docker ps -a --format "{{.Names}}" | grep bubly | xargs -r docker rm -f || true
echo

echo "### Downloading recommended TLS parameters if missing ..."
docker-compose run --rm --entrypoint "sh -c \"if [ ! -s /etc/letsencrypt/options-ssl-nginx.conf ] || [ ! -s /etc/letsencrypt/ssl-dhparams.pem ]; then \
  mkdir -p /etc/letsencrypt; \
  python -c 'import urllib.request as u; u.urlretrieve(\\\"https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf\\\", \\\"/etc/letsencrypt/options-ssl-nginx.conf\\\")'; \
  python -c 'import urllib.request as u; u.urlretrieve(\\\"https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem\\\", \\\"/etc/letsencrypt/ssl-dhparams.pem\\\")'; \
fi\"" certbot

# Check if certificates exist already in the Docker volume
cert_exists=$(docker-compose run --rm --entrypoint "sh -c 'if [ -d /etc/letsencrypt/live/${domains[0]} ]; then echo 1; else echo 0; fi'" certbot | tr -d '\r')

if [ "$cert_exists" = "0" ]; then
    echo "### Creating dummy certificate for ${domains[0]} ..."
    path="/etc/letsencrypt/live/${domains[0]}"
    docker-compose run --rm --entrypoint "sh -c '\
      mkdir -p $path && \
      openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \\
        -keyout $path/privkey.pem \\
        -out $path/fullchain.pem \\
        -subj \"/CN=localhost\"'" certbot
    echo
fi

echo "### Starting nginx ..."
docker-compose rm -f -s nginx || true
docker-compose up -d nginx
echo

if [ "$cert_exists" = "0" ]; then
    echo "### Deleting dummy certificate for ${domains[0]} ..."
    docker-compose run --rm --entrypoint "sh -c '\
      rm -Rf /etc/letsencrypt/live/${domains[0]} && \
      rm -Rf /etc/letsencrypt/archive/${domains[0]} && \
      rm -Rf /etc/letsencrypt/renewal/${domains[0]}.conf'" certbot
    echo

    echo "### Requesting Let's Encrypt certificate for ${domains[0]} ..."
    domain_args=""
    for domain in "${domains[@]}"; do
        domain_args="$domain_args -d $domain"
    done

    case "$email" in
    "") email_arg="--register-unsafely-without-email" ;;
    *) email_arg="--email $email" ;;
    esac

    if [ $staging != "0" ]; then staging_arg="--staging"; fi

    docker-compose run --rm --entrypoint "\
      certbot certonly --webroot -w /var/www/certbot \
        $staging_arg \
        $email_arg \
        $domain_args \
        --rsa-key-size $rsa_key_size \
        --agree-tos \
        --non-interactive \
        --force-renewal" certbot
    echo

    echo "### Reloading nginx ..."
    docker-compose exec nginx nginx -s reload
fi

echo "### Starting the rest of the application stack ..."
# Re-apply the ContainerConfig workaround to the main stack
docker-compose rm -f -s api || true
docker-compose rm -f -s db || true
docker-compose rm -f -s nginx || true
docker-compose rm -f -s certbot || true
docker-compose up -d --build