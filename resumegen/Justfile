set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

output_resume_json := "./output"
output_resume_json_PRIVATE := "./output/PRIVATE"

cv_pdf  := "../files/cv/CV_SamuelWinslowStark.pdf"
# cv_docx := "../files/cv/CV_SamuelWinslowStark.docx"
cv_md   := "../_includes/cv/current.md"
cv_html := "../files/cv/CV_SamuelWinslowStark.html"

default:
    @just --list

[windows]
setup-js:
    nvm use 23.5.0
    npm install
    New-Item -Path .\output -ItemType Directory -Force
    New-Item -Path .\output\PRIVATE -ItemType Directory -Force

[unix]
setup-js:
    npm install
    mkdir -p ./output/
    mkdir -p ./output/PRIVATE

render-js-main name="current":
    uv run python ./buildcv.py -o {{output_resume_json}} resume.toml configs.toml

    npx resume-cli export {{cv_pdf}} -r {{output_resume_json}}/resume.{{name}}.json -t ./jsonresume-theme-turnipcaffeine
    npx resume-cli export {{cv_html}} -r {{output_resume_json}}/resume.{{name}}.json -t ./jsonresume-theme-turnipcaffeine

    uv run python ./rendermarkdown.py --include_basics {{output_resume_json}}/resume.current.json {{cv_md}}

render-js name="current":
    uv run python ./buildcv.py -o {{output_resume_json}} resume.toml configs.toml

    npx resume-cli export {{output_resume_json}}/CV_SamuelWinslowStark_{{name}}.pdf -r {{output_resume_json}}/resume.{{name}}.json -t ./jsonresume-theme-turnipcaffeine
    npx resume-cli export {{output_resume_json}}/CV_SamuelWinslowStark_{{name}}.html -r {{output_resume_json}}/resume.{{name}}.json -t ./jsonresume-theme-turnipcaffeine

    uv run python ./rendermarkdown.py --include_basics {{output_resume_json}}/resume.{{name}}.json {{output_resume_json}}/CV_SamuelWinslowStark_{{name}}.md 

render-js-PRIVATE name="current":
    uv run python ./buildcv.py -o {{output_resume_json_PRIVATE}} resume.toml configs.toml ./resumegen-private/configs.toml

    npx resume-cli export {{output_resume_json_PRIVATE}}/CV_SamuelWinslowStark_{{name}}_PRIVATE.pdf -r {{output_resume_json_PRIVATE}}/resume.{{name}}.json -t ./jsonresume-theme-turnipcaffeine
    npx resume-cli export {{output_resume_json_PRIVATE}}/CV_SamuelWinslowStark_{{name}}_PRIVATE.html -r {{output_resume_json_PRIVATE}}/resume.{{name}}.json -t ./jsonresume-theme-turnipcaffeine

# # Render the main CV with turnip_text
# render-main:
#     uv run python ./buildcv.py -o {{output_resume_json}} resume.toml configs.toml

#     # Render the main CV into the static files
#     uv run -- python -m turnip_text.cli render --setup CvSetup cv.ttext -o {{output_resume_json}} --formats markdown latex docx --setup-args resumejson:{{output_resume_json}}/resume.current.json
#     uv run -- latexmk -cd -lualatex -cd ./{{output_resume_json}}/cv.tex -auxdir=build
#     cp {{output_resume_json}}/cv.md {{cv_md}}
#     cp {{output_resume_json}}/cv.pdf {{cv_pdf}}
#     cp {{output_resume_json}}/cv.docx {{cv_pdf}}

# render-other name:
#     uv run python ./buildcv.py -o {{output_resume_json}} resume.toml configs.toml --config {{name}}
#     uv run -- python -m turnip_text.cli render --setup CvSetup cv.ttext -o {{output_resume_json}}/{{name}} --formats latex docx --setup-args resumejson:{{output_resume_json}}/resume.{{name}}.json
#     uv run -- latexmk -cd -lualatex -cd ./{{output_resume_json}}/{{name}}/cv.tex -auxdir=build

