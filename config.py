#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as ET

# Режим ручного управления
#
# В режиме ручного управления перед каждым следующим шагом запрашивается 
# подтверждение пользователя. Для продолжения нужно ввести "Y", "y" или 
# нажать Enter.
#
# При отключённом режиме ручного управления скрипт будет исполнять 
# последовательно шаг за шагом. 
# 
# Включить режим ручного управления
#
#     MANUAL_MODE = True
#
# Выключить режим ручного управления
#
#     MANUAL_MODE = False
#
MANUAL_MODE = True

# URL со списком CI джоб
#
# С этого адреса будут собраны все джобы, в которые нужно внести изменения.
CI_URL_PREFIX = "https://cisrv.yourcompany.com/user/arsu1014/my-views/view/Devpoint/"

# Флаг отключения сбора CI-джоб с Jenkins
#
# Установите USE_JOB_LIST = True, чтобы отключить сбор CI-джоб из CI_URL_PREFIX
# (предыдущий параметр).
USE_JOB_LIST = True
JOB_LIST_FILE = "modify.txt"

# Имя пользователя
#
# Доменный пользователь из-под которого будут делаться запросы к Jenkins. 
# Внутри yourcompany'а любые запросы ко всем серверам Jenkins CI должны 
# происходить из-под какого-либо доменного пользователя
USERNAME = "vama0616"

# Пароль
#
# Пароль доменного пользователя из-под которого будут делаться запросы к 
# Jenkins.
PASSWORD = "your_password"

# Имя папки с данными
# 
# При запуске скрипта будет создана директория в том же месте, где лежит 
# скрипт. В неё будут записываться логи, конфигурация CI джоб и вообще любые 
# файлы и данные, относящиеся к последнему запуску скрипта. Вы можете 
# установить любое статическое имя:
#
#     LOCAL_STORAGE_DIR = "process"
#
# или генерировать автоматически имя на каждый запуск скрипта отдельно. 
# Например, создавать папку, содержащую в имени дату и время запуска:
#     
#     LOCAL_STORAGE_DIR = "process-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#
LOCAL_STORAGE_DIR = "process-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


# Имя файла с логами
#
# Скрипт автоматического переконфигурирования CI джоб достаточно подробно 
# логирует действия и ошибки. Вся эта информация записывается в файл. Файл 
# всё время дополняется и никогда не удаляется, не переименовывается, не 
# заменяется новым. 
LOG_FILE_NAME = "log.txt"

# Имя директории с оригинальной конфигурацией CI джоб
#
# Перед редактированием кофигурации на Jenkins-серверах скрипт сохраняет 
# исходную конфигурацию модифицируемых CI джоб, чтобы позднее можно было её 
# восстановить, если что-то пойдёт не так. Исходная конфигурация хранится в
# виде XML файлов в директории:
# 
#     LOCAL_STORAGE_DIR/CI_JOBS_CONFIGS_DIR
#
CI_JOBS_CONFIGS_DIR = "jobs"

# Имя директории с модифицированной конфигурацией CI джоб
#
# Перед редактированием кофигурации на Jenkins-серверах скрипт вносит 
# изменения в исходную конфигурацию CI джоб локально. Модифицированная 
# конфигурация хранится в виде XML файлов в директории:
# 
#     LOCAL_STORAGE_DIR/CI_JOBS_RECONFIGS_DIR
#
CI_JOBS_RECONFIGS_DIR = "new_jobs"

# Действие
#
# Функция, выполняющая преобразование конфигурации. На вход получает файл.
# Возвращает модифицированную XML-конфигурацию как строку.
def action(job_config):
    SONAR_INSTALLATION_NAME = "sonar.yourcompany.com:8443"
    SONAR_ANALYSIS_PROPERTIES = '''sonar.projectKey=${SONAR_PROJECT_KEY}
sonar.branch=${SONAR_BRANCH}
sonar.projectName=${SONAR_PROJECT_NAME}
sonar.projectVersion=rev.${SVN_REVISION}
sonar.sources=./
sonar.java.sources=./
sonar.java.binaries=./
sonar.sourceEncoding=UTF-8
sonar.exclusions=**/*.html, **/*.htm, **/*.xml, **/*.xsd, **/*.ts, **/*.js, **/*.sql, **/*.css, **/*.inc
sonar.buildbreaker.queryMaxAttempts=60
sonar.buildbreaker.queryInterval=60000'''
    tree = ET.parse(job_config)
    root = tree.getroot()
    installation_name = root.find("./builders/hudson.plugins.sonar.SonarRunnerBuilder/installationName")
    if installation_name is not None:
        installation_name.text = SONAR_INSTALLATION_NAME
    else:
        sonar_runner_builder = root.find("./builders/hudson.plugins.sonar.SonarRunnerBuilder")
        instalation_name = ET.SubElement(sonar_runner_builder, 'installationName')
        instalation_name.text = SONAR_INSTALLATION_NAME
        #log("Warning: SONAR_INSTALLATION_NAME has not been found. Tag created manually")
    properties = root.find("./builders/hudson.plugins.sonar.SonarRunnerBuilder/properties")
    if properties is not None:
        properties.text = SONAR_ANALYSIS_PROPERTIES
    #else:
    #    log("Warning: SONAR_ANALYSIS_PROPERTIES has not been found")
    return ET.tostring(root, encoding='utf8').decode('utf8')