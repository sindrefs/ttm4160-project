#!/bin/bash

DTB=`pwd`

echo '*** MAKE SURE THAT THE THUNDERBORG SOFTWARE IS INSTALLED ***'

echo '=== Make scripts executable ==='
chmod a+x *.py
chmod a+x *.sh

echo '=== Finished ==='
echo ''
echo 'Your Raspberry Pi should now be setup for running DiddyBorg 2'
echo 'Please restart your Raspberry Pi to ensure the I2C driver is running'
