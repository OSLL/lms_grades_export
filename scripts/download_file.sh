#!/bin/bash

function download_csv() {
# usage: download_csv table_id sheet_id export_file_path
# csv-separatоr = ","
  table_id="$1"
  sheet_id=${2:-'0'}
  export_file=${3:-'export.csv'}
  wget -O $export_file "https://docs.google.com/spreadsheets/d/$table_id/export?gid=$sheet_id&format=csv"
}


function download_sheet() {
# usage: download_sheet table_id sheet_id export_filename export_file_extention
# https://gist.github.com/Spencer-Easton/78f9867a691e549c9c70
  table_id="$1"
  sheet_id=${2:-'0'}
  filename=${3:-'export'}
  extension=${4:-'pdf'}
  wget -O "$filename.$extension" "https://docs.google.com/spreadsheets/d/$table_id/export?gid=$sheet_id&format=$extension&fzr=true"
}