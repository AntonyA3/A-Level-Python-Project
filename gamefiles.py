
class Text_files:

    def __init__(self,name,file):
        """

        :param name: This is the
        :param file: This is the file path of this instance of Text_files
        """
        self.name=name
        self.file=file
    def read(self):
        """
        :return: The content of the file in the format of a string
        """
        file=open(self.file,"r")
        return file.read()
    def write(self,text):
        file = open(self.file, "w")

        file.write(text)

