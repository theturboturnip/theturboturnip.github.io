#!/usr/bin/env bash

python3.8 ./buildcv.py resume.json configs.json
npx resume-cli export ../files/cv/current.pdf -r ./output/resume.current.json -t ./jsonresume-theme-turnipcaffeine
npx resume-cli export ../files/cv/current.html -r ./output/resume.current.json -t ./jsonresume-theme-turnipcaffeine