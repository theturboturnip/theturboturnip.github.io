set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    @just --list

[windows]
prepare:
    bundle install
[macos]
prepare:
    asdf exec bundle install
[unix]
prepare:
    rbenv install
    bundle install

[windows]
debug_serve:
    bundle exec jekyll serve
[macos]
debug_serve:
    asdf exec bundle exec jekyll serve
[unix]
debug_serve:
    rbenv local
    bundle exec jekyll serve
