import json
from logger import logger
from question import Question
from random import shuffle

class QuestionDatabase(object):
    def __init__(self):
        self._questions = []

    def fromJsonFile(self, jsonFile):
        try:
            content = json.load(open(jsonFile))
        except ValueError as e:
            logger.error("Error while reading file %s:", jsonFile)
            logger.error(e)
        except IOError as e:
            logger.error("Error while parsing file %s:", jsonFile)
            logger.error(e)

        if "questions" not in content:
            logger.error("No field 'questions' found")
        for obj in content["questions"]:
            if not Question.validate(obj):
                logger.info("Skipping following question, see errors above:")
                logger.info(json.dumps(obj, sort_keys = True, indent = 2,
                    separators = (',', ': ')))
            else:
                self._questions += [Question(obj)]

    def sample_by_tag(self, tag, num, used=None):
        if used is None:
            used=[]
        questions = set(
            [question for question in self._questions if question.hasTag(tag)])
        questions = list(questions - set(used))
        shuffle(questions)
        if len(questions) < num:
            logger.warning(
                "Not enough questions with tag '%s' available.", tag)
            logger.warning("Adding %d instead of %d.", len(questions), num)
            return questions
        else:
            return questions[:num]
