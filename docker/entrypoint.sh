#!/bin/sh

# Start the initial program
/etc/init.d/postgresql restart
/etc/init.d/rabbitmq-server restart

# Execute the CMD
/bin/bash
