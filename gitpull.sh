#!/bin/bash
rm -f gitlog.txt
timeNow=$(date)
echo $timeNow >> gitlog.txt
git pull >> gitlog.txt
git log >> gitlog.txt