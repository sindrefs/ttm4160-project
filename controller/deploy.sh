#! /bin/bash

npm run build

aws s3 cp --recursive build/ s3://ttm4160ttm4160webstack64-ttm4160webbucketa0bea2e5-1pgrw4d9zjcpk/web