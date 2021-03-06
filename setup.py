#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
import os

__version__ = '1.0'  # Здесь можно менять глобальный мажор.минор вашего инструмента. Итоговая версия после сборки будет выглядеть так: [major.minor].[build] для релизных сборок и [major.minor.dev]build для нерелизных.
# В дальнейшем узнать версию вашего установленного инструмента внутри программы возможно используя метод, аналогичный этому:
# https://github.com/devopshq/FuzzyClassificator/blob/master/FuzzyClassificator.py#L27
# import pkg_resources  # часть стандартной библиотеки setuptools
# version = pkg_resources.get_distribution('YourProject').version

devStatus = '4 - Beta'  # Билд-статус по умолчанию, смотрите: https://pypi.python.org/pypi?%3Aaction=list_classifiers

# Логика версионирования в зависимости от веток настраивается ниже:
if 'TRAVIS_BUILD_NUMBER' in os.environ and 'TRAVIS_BRANCH' in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ['TRAVIS_BUILD_NUMBER']))
    print("TRAVIS_BRANCH = {}".format(os.environ['TRAVIS_BRANCH']))

    __version__ += '.{}{}'.format(
        '' if 'release' in os.environ['TRAVIS_BRANCH'] or os.environ['TRAVIS_BRANCH'] == 'master' else 'dev',
        os.environ['TRAVIS_BUILD_NUMBER'],
    )

    devStatus = '5 - Production/Stable' if 'release' in os.environ['TRAVIS_BRANCH'] or os.environ['TRAVIS_BRANCH'] == 'master' else devStatus

else:
    print("This is local build")
    __version__ += '.dev0'  # set version as major.minor.localbuild if local build: python setup.py install

print("Trial Project build version = {}".format(__version__))  # Перед сборкой выведется сообщение о том, какая версия собирается

#  Это основной раздел настроек setuptools для сборки вашей программы
setup(
    name='pt-test-issuesapp',  # имя проекта под которым люди будут искать вашу программу в PyPI и инсталлить через "pip install dohq-example-project"

    version=__version__,

    description='About This Project: https://github.com/antonzolotukhin/pt-test-issuesapp',  # короткое описание проекта - отображается рядом с пакетом в PyPI

    long_description='Project for CI practice learning purposes',  # подробная документация должна быть доступна в GitHub Pages по этой ссылке

    license='MIT',  # только MIT лицензия для Open DevOps Community

    author='Anton Zolotukhin',  # укажите имя основного автора, либо укажите Open DevOps Community

    author_email='anton.i.zolotukhin@gmail.com',  # е-mail автора либо ссылка на Open DevOps Community

    url='https://github.com/antonzolotukhin/pt-test-issuesapp',  # сюда пишем ссылку на GitHub Pages или другой сайт с документацией

    download_url='https://github.com/antonzolotukhin/pt-test-issuesapp.git',  # здесь указываем ссылку на проект в GitHub

    entry_points={'console_scripts': ['pt-test-issuesapp = pttestissuesapp.issuesapp:main']},  # Точка входа указывает на основной метод, который нужно запустить при запуске программы из консоли. Например, если основной модуль в пакете exampleproject называется Main, то в данном примере будет запущен метод Main() этого скрипта, если вы наберёте в консоли команду "exampleproject".

    classifiers=[  # все допустимые классификаторы для PyPI подробно перечислены на страничке: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: {}'.format(devStatus),
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.6',
    ],

    platforms=[
        'any'
    ],

    keywords=[  # перечислите все ключевые слова, которые ассоциируются с вашим инструментом, каждое слово отдельной записью
        'exampleproject',
        'devops',
    ],

    packages=[  # необходимо перечислить ВСЕ каталоги с пакетами, если они присутствуют в вашем проекте, либо оставить '.', что будет указывать на то, что корень проекта сам является пакетом (в корне должен быть __init__.py)
        'pttestissuesapp',
    ],

    setup_requires=[  # необходимо перечислить ВСЕ библиотеки, от которых зависит сборка вашего инструмента
        'pytest-runner',
    ],

    tests_require=[  # необходимо перечислить ВСЕ библиотеки, которые должны быть установлены для запуска тестов
        'requests',
        'pytest==3.1.2',
        'HTTPretty',
        'pytest_httpretty',
        'pytest-mock',

    ],

    install_requires=[  # необходимо перечислить ВСЕ библиотеки, от которых зависит ваш инструмент (requirements), кроме стандартных библиотек, и они будут установлены автоматически при установке вашего инструмента
        'requests',
    ],

    package_data={  # необходимо перечислить ВСЕ файлы, которые должны войти в итоговый пакет, например:
        '': [
            './pttestissuesapp/*.py',  # если проект содержит другие модули, их и все входящие в них файлы тоже нужно перечислить

            './tests/*.py',  # все юнит-тесты, если вы хотите, чтобы люди могли их запускать после установки вашей библиотеки
            './tests/resources/*/*/*/*.json'
            './tests/resources/*/*/*/*/*.json'
            'LICENSE',  # файл лицензии нужно добавить в пакет
            'README.md',  # файл документации нужно добавить в пакет
        ],
    },

    zip_safe=True,
)
