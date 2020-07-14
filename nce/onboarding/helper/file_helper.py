# -*- coding: utf-8 -*-


class FileHelper:

    @staticmethod
    def write_file(content, path):
        """
            Writes the content to a file

        :param content: Content that needs to be written to the file
        :param path: File path
        """
        with open(path, "wb") as file:
            file.write(content)
