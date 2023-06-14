# Webspectre

Quickly wrap your head around the HTML contents of a web page such as how many elements total, how many elements per, tree depth, available Xpaths, etc.

Simply run webspectre.py in the console, input a url and view the outputs (ultimately will have a single HTML output file, but for now it's mixture of outputs including console, text, etc.).

## Setup

Download a zip of the repo & unzip. Run webspectre.py using Python 3. Ensure you have the dependencies installed using `pip install -r requirements.txt`

## VSCode Settings

If using VSCode, here are the default settings I have for `.vscode` folder in the working directory (be sure to update the folder paths to your system). These settings are mainly to help with being able to run the VSCode debugger with Scrapy.

### Launch.json

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Launch Scrapy Spider",
            "type": "python",
            "request": "launch",
            "module": "scrapy",
            "python": "${workspaceFolder}\\..\\..\\pvenv\\webspectre\\Scripts\\python.exe",
            "args": [
                "runspider",
                "${file}"
            ],
            "console": "integratedTerminal"
        },
        // {
        //     "name": "Python: Current File",
        //     "type": "python",
        //     "request": "launch",
        //     "program": "${file}",
        //     "console": "integratedTerminal",
        // "python": "${workspaceFolder}\\..\\..\\pvenv\\webspectre\\Scripts\\python.exe",
        //     "justMyCode": true
        // },
    ]
}
```

### Settings.json

```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.autopep8"
    },
    "python.formatting.provider": "none"
}
```