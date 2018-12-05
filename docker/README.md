# Docker compose

## Install Docker Compose

See [Install Docker Compose](https://docs.docker.com/compose/install/)

## Configuration for app

```bash
cd config && cp config.py.default config.py && cd ..
```

## Configuration for project

See `.env`

## Create and run the project (an one-off command)

```bash
./create_proj_one_off.sh
```

## Init database (as needed)

```bash
./init_db.sh
```

## Set password for admin

```bash
./set_admin_password.sh
```

## Stop and destroy the project (an one-off command)

```bash
./destroy_proj_one_off.sh
```
