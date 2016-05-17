from logger import logger

class Config(object):
    def __init__(self, json):
        self.tags = json["tags"]
        self.nStudents = json["nStudents"]

    @staticmethod
    def validate(json):
        if "tags" not in json:
            logger.error("Config should have 'tags' field")
            return False
        if "nStudents" not in json:
            logger.error("Config should have 'nStudents' field")
            return False
        for tag in json["tags"].keys():
            if not tag:
                logger.error("Invalid tag")
                return False
        return True
