if exist build rmdir /s /q build
python update_version_yaml.py
pyivf-make_version --source-format yaml --metadata-source version.yaml --outfile version.txt
pyinstaller --onefile --noconsole --paths=./src --add-data "./src/view;view" --name GravityClock --icon assets/GravityClock.ico --version-file=version.txt src/main.py
