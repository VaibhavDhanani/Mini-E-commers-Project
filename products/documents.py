from django_elasticsearch_dsl import Document, Index, fields
from .models import Product
from datetime import datetime
from elasticsearch import Elasticsearch
from django.conf import settings


es = Elasticsearch(
    settings.ELASTICSEARCH_DSL["default"]["hosts"],
    basic_auth=settings.ELASTICSEARCH_DSL["default"]["http_auth"],
    verify_certs=False
)
product_index = Index('products')
search_index = Index('search_events')

product_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

search_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@product_index.doc_type
class ProductDocument(Document):

    name = fields.TextField(
        fields={
            'raw': fields.KeywordField()
        }
    )

    description = fields.TextField()
    price = fields.FloatField()
    is_active = fields.BooleanField()
    created_at = fields.DateField()

    class Django:
        model = Product
        fields = []



def log_search(query, products, user=None):
    es.index(
        index="search_events",
        document={
            "query": query,
            "product_ids": [p.id for p in products],
            "user_id": user.id if user else None,
            "timestamp": datetime.now(),
            "result_count": len(products),
        }
    )