import argparse
import json
import random
import sys
import string

from lib.config import Config
from lib.logger import logger
from lib.question_database import QuestionDatabase
from jinja2 import Template

if __name__ == '__main__':
    random.seed()

    parser = argparse.ArgumentParser(
        description='Multiple-choice exam generator')
    parser.add_argument('--questions', dest='questionsFile',
        metavar='file.json', type=str, nargs=1, help='Questions file (.json)',
        required=True)
    parser.add_argument('--config', dest='configFile', metavar='file.json',
        type=str, nargs=1, help='Configuration file (.json)', required=True)
    args = parser.parse_args()

    questionsFile = args.questionsFile[0]
    questionDatabase = QuestionDatabase()
    questionDatabase.fromJsonFile(questionsFile)

    configFile = args.configFile[0]
    try:
        content = json.load(open(configFile))
    except ValueError as e:
        logger.error("Error while reading file %s:", configFile)
        logger.error(e)
    except IOError as e:
        logger.error("Error while parsing file %s:", configFile)
        logger.error(e)
    if not Config.validate(content):
        logger.error("Could not parse config. See errors above.")
        sys.exit(0)
    config = Config(content)

    questions = []
    for (tag, num) in config.tags.items():
        questions += questionDatabase.sample_by_tag(tag, num, questions)

    correctAnswersTex = u'\\documentclass{article}\n'
    correctAnswersTex += u'\\usepackage{fullpage}'
    correctAnswersTex += u'\\begin{document}'
    correctAnswersTex += u'\\begin{tabular}{|l||' + 'c|' * len(questions) + '}\n'
    correctAnswersTex += u'\\hline\n'
    for documentId in xrange(1, config.nStudents + 1):
        random.shuffle(questions)

        for question in questions:
            random.shuffle(question.answers)

        correctAnswers = []
        for questionId, question in enumerate(questions):
            correctAnswerCode = ''
            for answerId, answer in enumerate(question.answers):
                if answer["correct"]:
                    correctAnswerCode += string.uppercase[answerId]
            correctAnswers += [correctAnswerCode]

        correctAnswersTex += (str(documentId) + u' & ' +
                u' & '.join(correctAnswers) + u' \\\\\n\\hline\n')

        #TODO: Use a template.
        documentTex = u'\\begin{enumerate}'
        for question in questions:
            documentTex += u'\\item ' + question.statement + u'\n'
            documentTex += u'  \\begin{itemize}\n'
            for answerId, answer in enumerate(question.answers):
                documentTex += u'    \\item[(%s)] %s' % (
                        string.lowercase[answerId], answer["text"])
            documentTex += '\\end{itemize}\n'
        documentTex += u'\\end{enumerate}'
        open('questions_%d.tex' % documentId, 'w').write(documentTex.encode('utf8'))

    correctAnswersTex += u'\\end{tabular}'
    correctAnswersTex += u'\\end{document}'

    open('correct_answers_grid.tex', 'w').write(correctAnswersTex.encode('utf8'))
