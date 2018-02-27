#!/bin/bash

# Exit when receiving SIGTERM (usefull when running the script from CLI)
trap 'exit 0' SIGTERM;

# If the config file does not exists, we create one with the sample values
if [ ! -f /config/Cleaner.conf ]; then
    echo "Creating sample config file...";
    python /app/PlexCleaner.py --dump "/config/Cleaner.conf";
fi

# Run the cleaning script every 5 minutes
while true; do 
    echo "$(date) - Running script";
    python /app/PlexCleaner.py --config "/config/Cleaner.conf"; 
    EXIT_STATUS_CODE=$?
    echo "Process existed with code ${EXIT_STATUS_CODE}"
    if [ ${EXIT_STATUS_CODE} != 0 ]; then 
        echo "An error occured, stop relaunching process..."; 
        exit "${EXIT_STATUS_CODE}";
    else 
        echo "Sleeping ${INTERVAL_IN_SECOND} seconds...";
        sleep $INTERVAL_IN_SECOND;
        echo "";
        echo "=========================================";
        echo "";
    fi
done


