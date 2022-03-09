#!/bin/bash
echo "Starting CherryPy..."
supervisord -c /stt/cherrypy.conf
sleep infinity