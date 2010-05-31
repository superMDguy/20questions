#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       model.py

import web
#import config
from config import db

def add_object(name):
    object_id = db.insert('objects', name=name)
    # initialize weights for each question in data
    questions = get_questions()
    for question in questions:
        add_data(object_id, question.id, 0) # this is inconsistent
    
    return object_id
        

def add_question(question):
    question_id = db.insert('questions', text=question)
    # initialize weights for each object in data
    objects = get_objects()
    for object in objects:
        add_data(object.id, question_id)
    return question_id

def add_data(object_id, question_id, value=0):
    db.insert('data', object_id=object_id, question_id=question_id, value=value)

def update_data(object_id, question_id, value):
    db.update('data', where='object_id = $object_id AND question_id = $question_id', vars=locals(), value=value)
    
def update_weights(object_id, asked_questions):
    # Dictionary {question: value}
    for question in asked_questions:
        value = asked_questions[question]
        update_data(object_id, question, value)

def get_value(object_id, question_id):
    where = 'object_id=%d AND question_id=%d' %(object_id, question_id)
    try:
        return db.select('data', vars=locals(), where=where)[0].value
    except IndexError:
        return None

def get_objects():
    return db.select('objects')
    
def get_data():
    return db.select('data')

def get_questions():
    return db.select('questions')

def flush_tables():
    db.query('DELETE FROM objects')
    db.query('DELETE FROM data')
    db.query('DELETE FROM questions')
    
def get_object_by_name(name):
    try:
        return db.select('objects', vars=locals(), where='name=$name')[0]
    except IndexError:
        return None

def get_object_by_id(id):
    try:
        return db.select('objects', vars=locals(), where='id = $id')[0]
    except IndexError:
        return None

def get_question_by_id(id):
    try:
        return db.select('questions', vars=locals(), where='id=$id')[0]
    except IndexError:
        return None ############ maybe 0?
        
def get_question_by_text(text):
    try:
        return db.select('questions', vars=locals(), where='text=$text')[0]
    except IndexError:
        return None

def get_data_by_question_id(question_id):
    try:
        return db.select('data', vars=locals(), where='question_id=$question_id')
    except IndexError:
        return None
        
def get_data_by_object_id(object_id):
    try:
        return db.select('data', vars=locals(), where='object_id=$object_id')
    except IndexError:
        return None

def update_times_played(object_id):
    current = db.select('objects', vars=locals(), where='id=$object_id')[0].times_played
    if current == None: current = 0
    db.update('objects', where='id = $object_id', vars=locals(), times_played=current+1)

def num_objects():
    return db.query('select COUNT(*) from objects;')

def record_playlog(object_id, asked_questions, right):
    db.insert('playlog', object_id=object_id, data=str(asked_questions), right=right)

def delete_question(question_id):
    db.delete('questions', where='id=$question_id', vars=locals())
    db.delete('data', where='question_id=$question_id', vars=locals())
    
def delete_object(object_id):
    db.delete('objects', where='id=$object_id', vars=locals())
    db.delete('data', where='object_id=$object_id', vars=locals())
