"""
Database communication
"""
import os

import mongomock
from flask_pymongo import PyMongo

mongo = None


class TaskRepository:
    """
    Class to communicate with Database and make operations.
    """
    def __init__(self, app):
        self.app = app

    def get_mongo_connection(self):
        """
        Method to initialize the MongoDB connection.
        :return: Mongodb connection instance.
        :rtype: PyMongo
        """
        global mongo

        if self.app.config['TESTING']:
            if mongo is None:
                mongo = mongomock.MongoClient()
            return mongo
        else:
            if 'MONGO_URI' not in self.app.config:
                self.app.config['MONGO_URI'] = "mongodb://"\
                              + os.environ['MONGODB_USERNAME']\
                              + ":" + os.environ['MONGODB_PASSWORD']\
                              + "@" + os.environ['MONGODB_HOSTNAME']\
                              + "/" + os.environ['MONGODB_DATABASE']

            if not mongo:
                mongo = PyMongo(self.app)

            return mongo

    def drop_mongo_connection(self):
        """

        :return: Returns the Mongo Instance.
        :rtype: mongo
        """
        if self.app.config['TESTING']:
            if mongo:
                mongo.drop_database('db')
        return mongo
    
    def find_all(self):
        query_result = self.get_mongo_connection().db.task.find()
        tasks = []
        for task in query_result:
            tasks.append(task)
        return tasks

    def find_by_id(self, task_id):
        return self.get_mongo_connection().db.task.find_one({"_id": task_id})

    def find_available_id(self):
        """
        Method that returns the next Identifier available to be used.
        Query the max Identifier in the Database, and increase one more.
        :return: Integer Identifier available to be use.
        :rtype: int
        """
        query_result = self\
            .get_mongo_connection().db.task.find({}, {"_id": True})\
            .sort("_id", -1).limit(1)
        for obj in query_result:
            return obj.get('_id') + 1
        else:
            return 1

    def insert(self, task_serialized):
        return self.get_mongo_connection().db.task.insert_one(task_serialized)

    def update_by_id(self, task_id, task_serialized):
        return self.get_mongo_connection()\
            .db.task.update_one({"_id": task_id}, {"$set": task_serialized})

    def delete_by_id(self, task_id):
        return self.get_mongo_connection()\
            .db.task.delete_one({"_id": task_id})
