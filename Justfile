set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    @just --list

[windows]
prepare:
    bundle install
[macos]
prepare:
    asdf exec bundle install
[linux]
prepare:
    rbenv install -s
    bundle install

[windows]
debug_serve:
    bundle exec jekyll serve --drafts
[macos]
debug_serve:
    asdf exec bundle exec jekyll serve --drafts
[linux]
debug_serve:
    rbenv local
    bundle exec jekyll serve --drafts
