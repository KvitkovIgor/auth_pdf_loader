#!/bin/bash

while true; do eval "$(cat /Users/sprili/Desktop/Dev/auth_pdf_loader/dockerpipe)" &> ./outputs/logs.txt; done