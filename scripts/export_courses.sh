#!/bin/bash

# usage function in other script:
# source ./scripts/export_courses.sh
# exports=(
#   'humanreadable_subject;table_id;sheet_name;system;exportinfo'
# )
# system: "moodle" - Предмет;1zG21U9zJHIkfAM5ejd8WBw;Онлайн-курс;moodle;course_id
# system: "stepik" - Прудмет;1zG21U9zJHIkfAM5ejd8WBw;Онлайн-курс;stepik;course_id;class_id
# exportCourses "${exports[@]}"

function exportCourses() {
    exports=("$@")
    
    for line in "${exports[@]}"; do
        IFS=',' read -r -a current_export <<< "$line"

        echo "Экспорт для дисциплины ${current_export[0]} из ${current_export[3]} в таблицу ${current_export[1]} на лист ${current_export[2]}"

        if [[ "${current_export[3]}" == "moodle" ]]; then
            docker run --rm -v $google_conf:/app/conf.json moodle_export_parser:latest \
              --moodle_token $moodle_token --url https://e.moevm.info \
              --csv_path grades --google_token conf.json \
              --course_id ${current_export[4]} \
              --table_id ${current_export[1]} \
              --sheet_id ${current_export[2]} \
              --options github

            return_code=$?
        fi

        if [[ "${current_export[3]}" == "stepik" ]]; then

            docker run --rm -v $google_conf:/app/conf.json stepik_export_parser:latest \
              --client_id $stepik_client_id --client_secret $stepik_client_secret \
              --url https://stepik.org:443/api \
              --csv_path grades --google_token conf.json \
              --course_id ${current_export[4]} \
              --class_id ${current_export[5]} \
              --table_id ${current_export[1]} \
              --sheet_id ${current_export[2]}

            return_code=$?

        fi

        if [[ "${current_export[3]}" == "checker" ]]; then
            echo "Not implemented"
            return_code=1
        fi

        if [[ "$return_code" -ne "0" ]]; then
            exit 1
        fi

    done
}

function download_csv() {
# usage: download_csv table_id [sheet_id:0] [export_file_path]
  table_id="$1"
  sheet_id=${2:-'0'}
  export_file=${2:-'export.csv'}
  wget -O $export_file "https://docs.google.com/spreadsheets/d/$table_id/export?gid=$sheet_id&format=csv"
}
