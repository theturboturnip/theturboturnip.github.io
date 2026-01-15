set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    @just --list

[windows]
prepare:
    bundle install
[unix]
prepare:
    asdf exec bundle install

[windows]
debug_serve:
    bundle exec jekyll serve
[unix]
debug_serve:
    asdf exec bundle exec jekyll serve