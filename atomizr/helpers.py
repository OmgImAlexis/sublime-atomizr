import sublime

class Helpers():

    def rename_file(self, extension):
        if sublime.load_settings('Atomizr.sublime-settings').get("rename_files") != True:
            return

        import os

        inputFile = self.view.window().active_view().file_name()
        parentDir = os.path.dirname(inputFile)
        baseName = os.path.splitext(os.path.basename(inputFile))[0]
        fileName = baseName + "." + extension
        outputFile = os.path.join(parentDir, fileName)
        os.rename(inputFile, outputFile)

        self.view.set_name(fileName)
        self.view.retarget(outputFile)
        self.view.window().run_command("save")

    def add_trailing_tabstop(input):
        import re

        m = re.search(r'\$\d+$', input)

        if m is not None or sublime.load_settings('Atomizr.sublime-settings').get("add_trailing_tabstops") == False:
            # nothing to do here
            return input

        return input + "$0"

    def remove_trailing_tabstop(input):
        import re

        m = re.search(r'\$\d+$', input)

        if m is None or sublime.load_settings('Atomizr.sublime-settings').get("remove_trailing_tabstops") == False:
            # nothing to do here
            return input

        # remove tabstop
        return re.sub(r'\$\d+$', "", input)

    def set_xml(this):
        if sublime.version() >= "3103":
            this.view.set_syntax_file('Packages/XML/XML.sublime-syntax')
        else:
            this.view.set_syntax_file('Packages/XML/XML.tmLanguage')

        # this.rename_file(this)

    def set_json(this):
        if sublime.version() >= "3103":
            this.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            this.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        # this.rename_file(this)

    def get_coffee(this):
        import os

        # package locations
        locations = [sublime.installed_packages_path(), sublime.packages_path()]

        # supported packages
        packages = ["Better CoffeeScript", "CoffeeScript", "IcedCoffeeScript", "Mongoose CoffeeScript"]

        # iterate over packages locations
        for location in locations:
            # iterate over packages installed with Package Control
            for package in packages:
                # is "ignored_package"?
                settings = sublime.load_settings('Preferences.sublime-settings').get("ignored_packages")
                if package in settings:
                    continue

                if os.path.isfile(location + "/" + package + ".sublime-package") is True:
                    if package is "IcedCoffeeScript":
                        this.view.set_syntax_file("Packages/IcedCoffeeScript/Syntaxes/IcedCoffeeScript.tmLanguage")
                        return True
                    elif package is "Mongoose CoffeeScript":
                        this.view.set_syntax_file("Packages/Mongoose CoffeeScript/CoffeeScript.tmLanguage")
                        return True
                    else:
                        this.view.set_syntax_file("Packages/" + package + "/CoffeeScript.tmLanguage")
                        return True

        sublime.message_dialog("Atomizr\n\nAutomatic conversion requires a supported CoffeeScript package to be installed")
        return False

    def select_scope(this, target, meta):

        if target is "atom":
            if sublime.load_settings('Atomizr.sublime-settings').get("atom_json_snippets") is True:
                verticalPos = this.view.size()
                selectionStart = 5
            else:
                verticalPos = 0
                selectionStart = len(meta) + 1
            selectionEnd = selectionStart + len(".source")
        else:
            verticalPos = this.view.size()
            selectionEnd = verticalPos - 3
            selectionStart = selectionEnd - len(".source") + 1


        newSelection = sublime.Region( selectionStart, selectionEnd )

        # Selected scope
        this.view.selection.clear()
        this.view.selection.add( newSelection )

        # Scroll to scope definition
        this.view.set_viewport_position( [0, verticalPos] )

        sublime.status_message("Could not determine scope automatically")

    def reset_selection(this):
        this.view.selection.clear()
        this.view.selection.add( sublime.Region( 0, 0 ) )
