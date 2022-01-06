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

        version = "Not defined"
        icon = "unknown-preset.png"
        description = "Not defined"
        if "description" in packagejson:
            description = packagejson["description"]
        if "version" in packagejson:
            version = packagejson["version"]
        
        if "icon" in packagejson:
            newname = packagejson["name"] + "-" + version
        
            copyicon(newname, packagejson["icon"])
            icon = newname + ".png"
        if "contributes" in packagejson:
            if "themes" in packagejson["contributes"]:
                for theme in packagejson["contributes"]["themes"]:

                    name = theme["label"]
                    type = theme["uiTheme"]
                    print("Extracting theme", theme["label"])

                    pathh = os.path.join("./extracted/extension", os.path.normpath(theme["path"]))

                    with open(pathh) as f:
                        theme_file = json.load(f)
                        preset = {
                            "name": name,
                            "type": type,
                            "description": description,
                            "version": version,
                            "icon": "./preset-icons/" + icon,
                        }
                        if "colors" in theme_file:
                            preset["colors"] = theme_file["colors"]
                        if "semanticHighlighting" in theme_file:
                            preset["semanticHighlighting"] = theme_file["semanticHighlighting"]
                        if "tokenColors" in theme_file:
                            if isinstance(theme_file["tokenColors"], list):
                                preset["tokenColors"] = theme_file["tokenColors"]
                            else:
                                print("Error: tokenColors is not a list in theme " + name)
                                continue

                        if "semanticTokenColors" in theme_file:
                            preset["semanticTokenColors"] = theme_file["semanticTokenColors"]
                        with open("./presets/" + formatname(name) + ".tstudio-preset", "w") as f:
                            f.writelines(json.dumps(preset, indent=2))
       
        else:
            print("Error: package.json is missing contributes")
            sys.exit(2)

def copyicon(newname, icon):
    path = os.path.join("./extracted/extension", os.path.normpath(icon))
    shutil.copy(path, './preset-icons/' + newname + ".png")
def formatname(name):
    return name.replace(" ", "-").replace("(", "").replace(")", "").lower()

if __name__ == "__main__":

    main(sys.argv[1:])
