#/bin/bash

if [[ -z "${1}" ]]
then
    echo "Missing parameter"
fi

pylintExclusions='C0200,C0303,C0411,C0413,C0415,W0511,W0702,W0718,W0719,R0801,R0901,R0902,R0913,R0904,R0903,W0223'
pylintCmd="source /var/local/bin/stocks_venv/bin/activate; python -m pip install --quiet pylint; pylint --disable ${pylintExclusions} \$(find ./ -name '*.py' | grep -vP '(migrations|tests)')"
coverageCmd='source /var/local/bin/stocks_venv/bin/activate; coverage run manage.py test'
coverageReport='source /var/local/bin/stocks_venv/bin/activate; coverage report --omit="*/tests/*" -m'
case "${1}" in
    "pylint")
        docker exec stocks_backend /bin/bash -c "${pylintCmd}"
        ;;
    "pycoverage")
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
        docker exec stocks_backend /bin/bash -c "${coverageCmd}"
        docker exec stocks_backend /bin/bash -c "${coverageReport}"
        ;;                
esac