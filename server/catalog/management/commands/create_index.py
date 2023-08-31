from django.core.management.base import BaseCommand

from elasticsearch_dsl import connections

from catalog.constants import ES_INDEX


class Command(BaseCommand):
    help = 'Creates an Elasticsearch index.'

    def handle(self, *args, **kwargs):
        self.stdout.write(f'Creating index "{ES_INDEX}"...')
        connection =  connections.get_connection()
        if connection.indices.exists(index=ES_INDEX):
            self.stdout.write(f'Index "{ES_INDEX}" already exists')
        else:
            connection.indices.create(index=ES_INDEX, body={
                'settings': {
                    'number_of_shards': 1,
                    'number_of_replicas': 0,
                }
            })
            self.stdout.write(f'Index "{ES_INDEX}" created successfully')
