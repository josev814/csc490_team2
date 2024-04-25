#/bin/bash

pylintExclusions='C0103,C0200,C0201,C0206,C0303,C0411,C0413,C0415,W0511,W0702,W0718,W0719,R0801,R0901,R0901,R0902,R0913,R0914,R0904,R0903,E1101,W0223,W1203'
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
    - eslint
    - reacttest | jest
    - react (this runs eslint and react tests)

Example:
    bash run_in_containers.sh pycoverage users"

    exit
}

function react_lint(){
    docker exec stocks_frontend /bin/bash -c 'cd src; npx eslint $(find ./ -name "*.js" | grep -vP ".test.js")' > eslint.results.log
    if [[ $(grep -P '[0-9]+ problems' eslint.results.log | wc -l ) -gt 0 ]]; then
        echo "########## ESLint found errors ################"
    fi
    cat eslint.results.log
}

function react_unittests(){
    docker exec stocks_frontend /bin/bash -c 'cd src; npm test -- --coverage' > jest.results.log 2>&1
    if [[ $(grep -P '^Tests:\s+[0-9]+ failed,' jest.results.log | wc -l) -gt 0 ]]; then
        echo '################# UnitTests Failed ####################'
    fi
    cat jest.results.log
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
    "eslint")
        react_lint
        ;;
    "reacttest" | "jest")
        react_unittests    
        ;;
    "react")
        react_lint
        react_unittests
        ;;
    *|"--help")
        usage
        ;;
esac