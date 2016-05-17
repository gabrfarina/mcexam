from logger import logger
from hashlib import sha1

class Question(object):
    def __init__(self, json):
        self.statement = json["statement"]
        self.tags = json["tags"]
        self.answers = json["answers"]
        self.type = json["type"]

        self._hash = sha1()
        self._hash.update(str(json))
        self._hash = self._hash.hexdigest()

    def __hash__(self):
        return int(self._hash, 16)

    def hasTag(self, tag):
        return tag == '_any_' or tag in self.tags

    @staticmethod
    def validate(json):
        if "statement" not in json:
            logger.error("Question should have 'statement' field")
            return False
        if "tags" not in json:
            logger.error("Question should have 'tags' field")
            return False
        if "answers" not in json:
            logger.error("Question should have 'answers' field")
            return False
        if "type" not in json:
            logger.error("Question should have 'type' field")
            return False

        if not json["statement"]:
            logger.error("Question statement is empty")
            return False
        if not json["tags"]:
            logger.error("No tags defined")
            return False
        for tag in json["tags"]:
            if not tag:
                logger.error("Invalid tag")
                return False
            if tag == "_any_":
                logger.error("Don't use reserved tag '_any_'")
                return False
        if not json["answers"]:
            logger.error("No answer defined")
            return False
        for answer in json["answers"]:
            if 'text' not in answer:
                logger.error("Answer whould have 'text' field")
                return False
            if 'correct' not in answer:
                logger.error("Answer whould have 'correct' field")
                return False
        if not json["type"]:
            logger.error("No type declared")
            return False
        if json["type"] not in ("single", "multiple"):
            logger.error(
                "Question type is invalid. Use 'single' or 'multiple'")
            return False

        correctAnswers = [
            answer for answer in json["answers"] if answer["correct"]]
        if json["type"] == "single" and len(correctAnswers) is not 1:
            logger.error("Exactly one answer should be marked as correct")
            return False
        return True
