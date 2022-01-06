#!/usr/bin/python

import sys, getopt, os
import zipfile
import json
import shutil


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ht:", ["theme="])
    except getopt.GetoptError:
        print("preset.py -theme <vsix file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("preset.py -theme <vsix file>")
            sys.exit()
        elif opt in ("-t", "--theme"):
            unzip(arg)
            readpackage()
            cleanup()


def cleanup():
    try:
        shutil.rmtree("./extracted")
        print("Cleaned up")
    except OSError as e:
        print("Error: %s : %s" % ("./extracted", e.strerror))


def unzip(f):
    try:
        with zipfile.ZipFile(f) as z:
            print("Extracting to ./extracted")
            z.extractall("./extracted")
    except:
        print("Error: Cannot open file")


def readpackage():
    print("Reading package.json")
    with open("./extracted/extension/package.json") as f:
        packagejson = json.load(f)

        if "contributes" in packagejson:
            if "themes" in packagejson["contributes"]:
                for theme in packagejson["contributes"]["themes"]:
                    print(theme["uiTheme"], theme["path"])
                    extracttheme(theme)
        else:
            print("Error: package.json is missing contributes")
            sys.exit(2)


def extracttheme(theme):
    print("Extracting theme", theme["label"])
  
    pathh = os.path.join("./extracted/extension", os.path.normpath(theme["path"]))
    
    with open(pathh) as f:
        theme_file = json.load(f)
        print(theme_file)
    # with zipfile.ZipFile('./extracted/extension/' + theme['path']) as z:
    #   z.extractall('./extracted/extension/' + theme['path'])


if __name__ == "__main__":
    main(sys.argv[1:])
