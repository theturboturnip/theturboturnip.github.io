set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    @just --list

prepare:
    bundle install

debug_serve:
    bundle exec jekyll serve