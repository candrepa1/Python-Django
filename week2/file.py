class File:
    def __init__(self):
        self.filename = ""
        self.file = ""

    def read_filename(self, filename):
        self.filename = filename

    def open_file(self):
        try:
            file_opened = open(self.filename)
            self.file = file_opened
        except FileNotFoundError:
            print("File was not found")


if __name__ == '__main__':
    file = File()
    file.read_filename("f.txt")
    file.open_file()
    print(file.file)


