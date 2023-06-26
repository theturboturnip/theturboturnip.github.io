#!/usr/bin/env bash

# should be min. 3.8
PYTHON=python3

mkdir -p ./output/

$PYTHON ./buildcv.py resume.json configs.json
npx resume-cli export ../files/cv/current.pdf -r ./output/resume.current.json -t ./jsonresume-theme-turnipcaffeine
npx resume-cli export ../files/cv/current.html -r ./output/resume.current.json -t ./jsonresume-theme-turnipcaffeine

$PYTHON ./rendermarkdown.py ./output/resume.current.json ../_includes/cv/current.md