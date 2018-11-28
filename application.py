#!/usr/bin/env python
import os

from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restplus import Resource, Api

from challenge import articles


application = Flask(__name__)
application.config['MONGO_URI'] = os.environ.get('MONGO_URI')
api = Api(application, prefix='/api/challenge-v1')
mongo = PyMongo(application)


class Search(Resource):
    @api.doc(params={'include': 'include search keywords', 'exclude': 'exclude search keywords'})
    def get(self):
        try:
            results = articles.search_by_keyword(
                mongo.db.cleansed,
                **self._parsed_query(request.args))
        except Exception as e:
            return {'status': 'failed', 'error': '{}'.format(e)}, 400
        return self._format_results(results), 200

    @classmethod
    def _parsed_query(cls, args):
        return {
            'include': args.get('include', '').split(),
            'exclude': args.get('exclude', '').split(),
        }

    @classmethod
    def _format_results(cls, results):
        """
        Strip non-serializable items from records and return articles json.
        """
        results = [x for x in results if x.pop('_id')]
        return {
            'status': 'ok',
            'articles': results,
            'message': 'Found {} articles'.format(len(results))
        }


api.add_resource(Search, '/search')

if __name__ == '__main__':
    application.run(debug=True)
