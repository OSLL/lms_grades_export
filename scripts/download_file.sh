#!/bin/bash

function download_csv() {
# usage: download_csv table_id sheet_id export_file_path
# csv-separatоr = ","
  table_id="$1"
  sheet_id=${2:-'0'}
  export_file=${3:-'export.csv'}
  wget -O $export_file "https://docs.google.com/spreadsheets/d/$table_id/export?gid=$sheet_id&format=csv"
}


function download_sheet_to_pdf() {
# usage: download_sheet_to_pdf table_id sheet_id export_file_path
  table_id="$1"
  sheet_id=${2:-'0'}
  export_file=${3:-'export.pdf'}
  wget -O $export_file "https://docs.google.com/spreadsheets/d/$table_id/export?gid=$sheet_id&format=csv"
}