import sys, os
import json

import graphene

from query import EntityQuery
from mutation import EntityMutation
from docs import get_docs

def main():
    
    if len(sys.argv) < 2:
        print('There is no query')
        sys.exit()

    query = sys.argv[1]

    if query == 'docs':
        print(get_docs())
        print('====')
        return

    schema = graphene.Schema(query = EntityQuery, mutation = EntityMutation)

    print(json.dumps(schema.execute(query).data, indent = 4, sort_keys = True))
    print('====')

if __name__ == '__main__':
    main()