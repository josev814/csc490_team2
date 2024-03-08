#/bin/bash

pylintExclusions='C0200,C0201,C0206,C0303,C0411,C0413,C0415,W0511,W0702,W0718,W0719,R0801,R0901,R0901,R0902,R0913,R0914,R0904,R0903,E1101,W0223,W1203'
pylintCmd="source /var/local/bin/stocks_venv/bin/activate; python -m pip install --quiet pylint; pylint --disable ${pylintExclusions} \$(find ./ -name '*.py' | grep -vP '(migrations|tests)')"
coverageCmd='source /var/local/bin/stocks_venv/bin/activate; coverage run manage.py test'
coverageReport='source /var/local/bin/stocks_venv/bin/activate; coverage report --omit="*/tests/*" -m'
removeTestDB='mysql -u ${MYSQL_USER} -h ${MYSQL_HOST} -e "drop database if exists test_stocksapp"'

function usage(){
    echo "
Run this script in WSL and pass in an argument
Supported Arguments:
    - pylint
    - pycoverage (optional argument to pycoverage is the app to run tests against)
    - pycovreport
    - django (this runs pylint, pycoverage and pycovreport)

Example:
    bash run_in_containers.sh pycoverage users"

    exit
}

case "${1}" in
    "pylint")
        docker exec stocks_backend /bin/bash -c "${pylintCmd}"
        ;;
    "pycoverage")
        docker exec stocks_backend /bin/bash -c "${removeTestDB}"
        if ! [[ -z "${2}" ]]
        then
            docker exec stocks_backend /bin/bash -c "${coverageCmd} ${2}"
        else
            docker exec stocks_backend /bin/bash -c "${coverageCmd}"
        fi
        ;;
    "pycovreport")
        docker exec stocks_backend /bin/bash -c "${coverageReport}"
        ;;
    "django")
        docker exec stocks_backend /bin/bash -c "${pylintCmd}"
        docker exec stocks_backend /bin/bash -c "${removeTestDB}"
        docker exec stocks_backend /bin/bash -c "${coverageCmd}"
        docker exec stocks_backend /bin/bash -c "${coverageReport}"
        ;;
    *|"--help")
        usage
        ;;
esac