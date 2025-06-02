#!/bin/bash

function teardown(){
    docker compose -f "BuildTools/docker-compose.yml" down --volumes --remove-orphans
    if [[ $? -eq 1 ]]
    then
        echo "Failed to perform docker compose teardown"
        echo "Is Docker Desktop running?"
        exit
    fi
}

function standup(){
    docker compose -f "BuildTools/docker-compose.yml" up -d --build --remove-orphans
    if [[ $? -eq 1 ]]
    then
        echo "Failed to perform docker compose up"
        echo "Is Docker Desktop running?"
        exit
    fi
    cleanup_dangling_images
}

function does_image_exist(){
    docker image ls --filter="reference=$1" | grep -v 'REPOSITORY' | wc -l
}

function cleanup_compose_images(){
    echo "Cleanup up Compose Images"
    for compose_image in $(grep 'image:' BuildTools/docker-compose.yml | awk '{ print $2 }')
    do
        if [[ $(does_image_exist "${compose_image}") -gt 0 ]]
        then
            echo "Removing ${compose_image}"
            docker rmi "${compose_image}"
        fi
    done
}

function cleanup_dockerfile_images(){
    echo "Cleaning up dockerfile images"
    for image_tag in $(grep -ri '^FROM' ./**/docker* | awk '{ split($0, a, "FROM "); split(a[2], it, " AS "); print it[1]}')
    do
        if [[ $( does_image_exist "${image_tag}" ) -ne 0 ]]
        then
            docker rmi "${image_tag}"
        fi
    done
}

function cleanup_dangling_images(){
    echo "Cleaning up dangling images"
    if [[ $(docker images -f "dangling=true" -q | wc -l ) -gt 0 ]]
    then
        docker rmi $(docker images -f "dangling=true" -q)
    fi
}

function cleanup_volumes(){
    echo "Cleaning up volumes"
    docker volume rm dbdata redisdata -f
    docker volume prune -f
}

function cleanup_builder(){
    echo "Cleaning up builder"
    docker builder prune -af --verbose
    docker buildx prune -af --verbose
}

function cleanup(){
    cleanup_compose_images
    cleanup_dockerfile_images
    cleanup_dangling_images
    cleanup_volumes
    cleanup_builder
}

function get_logs(){
    echo "Exporting Container Logs"
    mkdir -p logs
    docker compose -f "BuildTools/docker-compose.yml" logs > logs/container_logs.log
}

function help(){
    echo "Please pass a parameter to this script"
    echo "teardown, cleanup, standup or getlogs"
    echo "You can also pass each of the parameters together"
    echo "They must be in the order of teardown cleanup standup getlogs"
    exit
}

if [ -z "${1}" ]
then
    help
fi

for i in {1..4}
do
    if [[ $i -eq 1 ]] && [[ -z "${!i}" ]]
    then
        help
    fi
    if [[ -z "${!i}" ]]
    then
        break
    fi
    case "${!i}" in
        teardown)
            teardown
            ;;
        cleanup)
            cleanup
            ;;
        standup)
            standup
            ;;
        getlogs)
            get_logs
            ;;
        *)
            help
            ;;
    esac
done