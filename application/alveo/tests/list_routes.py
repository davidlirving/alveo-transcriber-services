import uuid
import json
import random

from application import db
from application.users.model import User
from application.datastore.model import Datastore

from application.alveo.module import DOMAIN
from .alveo import AlveoTests


class AlveoListRoutesTests(AlveoTests):
    def testGetList(self):
        DATA_AMOUNT = 12
        for i in range(DATA_AMOUNT):
            self.postRandomData(domain=DOMAIN)

        response, status = self.get_json_response(
            DOMAIN + '/datastore/list/', self.DEFAULT_HEADERS)

        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid list while logged in.')

        self.assertEqual(
            len(response['storage_objects']),
            DATA_AMOUNT,
            'Expected to get a list matching the amount of items that were just posted.')

    def testGetListByKey(self):
        DATA_AMOUNT = 6
        DATASET_AMOUNT = 2

        posts = []
        responses = []

        for i in range(DATASET_AMOUNT):
            posts.append(
                (self.postRandomData, {
                    'return_sample': True, 'domain': DOMAIN}))

        for i in range(DATA_AMOUNT):
            posts.append(
                (self.postRandomData, {
                    'return_sample': True, 'domain': DOMAIN}))

        random.shuffle(posts)

        for post in posts:
            function, args = post
            response_query, dataset = function(**args)
            response, status = response_query
            self.assertEqual(
                200,
                status,
                'Expected OK status when attempting to post valid data while logged in.')

            if args['return_sample']:
                responses.append((dataset, response))

        response, status = self.get_json_response(
            DOMAIN + '/datastore/list/%s' % responses[0][0]['key'], self.DEFAULT_HEADERS)
        self.assertEqual(
            response['storage_objects'][0]['id'],
            responses[0][1]['id'],
            'Expected response to contain the storage object that was just posted.')

        response, status = self.get_json_response(
            DOMAIN + '/datastore/list/%s' % responses[0][0]['key'], self.DEFAULT_HEADERS)
        self.assertEqual(
            response['storage_objects'][0]['id'],
            responses[0][1]['id'],
            'Expected response to contain the storage object that was just posted.')

        response, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s' % responses[0][1]['id'], self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(response['key'], responses[0][0]
                         ['key'], 'Expected the newly added keys to match.')

        response, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s' % responses[0][1]['id'], self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(response['key'], responses[0][0]
['key'], 'Expected the newly added keys to match.')

    def testOtherUserList(self):
        self.generateSampleAlveoData()
        users = User.query.filter(User.domain == DOMAIN).all()

        # Note: Our user doesn't exist yet since the database is rebuilt each
        #  time. We'll only be added after our first successful request. So we can use whoever
        # we want from the sample pool without risk of getting our own test
        # user.

        self.assertTrue(
            len(users) > 0,
            "Expected sample users to exist from generated sample data.")

        user_1 = users[0].id
        user_2 = users[1].id

        transcription_list_1 = Datastore.query.filter(
            Datastore.user_id == user_1).all()
        transcription_list_2 = Datastore.query.filter(
            Datastore.user_id == user_2).all()
        transcription_1 = transcription_list_1[0]
        transcription_2 = transcription_list_2[0]

        db.session.expunge_all()

        self.assertTrue(
            len(transcription_list_1) > 0,
            "Expected sample transcriptions to exist from generated sample data.")
        self.assertTrue(
            len(transcription_list_2) > 0,
            "Expected sample transcriptions to exist from generated sample data.")

        response, status = self.get_json_response(
            DOMAIN + '/datastore/listall/%s' % user_1, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(len(response['storage_objects']), len(
            transcription_list_1), 'Expected the newly added keys to match.')

        response, status = self.get_json_response(
            DOMAIN + '/datastore/listall/%s' % user_2, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(len(response['storage_objects']), len(
            transcription_list_2), 'Expected the newly added keys to match.')

        query_key = transcription_2.key.split(':')[1]
        response, status = self.get_json_response(
            DOMAIN + '/datastore/listall/%s' %
            user_2, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')

        query_key = response['storage_objects'][0]['id']
        response, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s' %
            query_key, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')

        self.assertEqual(len(str(response['transcription'])), len(transcription_2.get_value(
        )), 'Expected the queried data to match the other user\'s data.')

    def testOtherDomainListFail(self):
        self.generateSampleAlveoData()

        user = User.query.filter(User.domain == DOMAIN).first()
        self.assertTrue(
            user is not None,
            "Expected sample users to exist from generated sample data.")

        # Change the user's domain
        user.domain = "notalveo"
        db.session.commit()

        response, status = self.get_json_response(
            DOMAIN + '/datastore/listall/%s' %
            user.id, self.DEFAULT_HEADERS)
        self.assertEqual(
                status,
                403,
                'Expected forbidden status when attempting to list store from a different user on another domain, while logged in.')
