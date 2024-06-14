#!/bin/bash
set -e

#tail -f ./logs/es_job_interface_api.log
sudo journalctl -u es_job_interface_api.service -f