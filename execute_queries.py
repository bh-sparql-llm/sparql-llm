import click as ck
import requests
import json
from pathlib import Path

@ck.command()
@ck.option('--queries-file', '-qf', help='An input file with SPARQL queries')
@ck.option('--output-folder', '-of', help='Output folder')
def main(queries_file, output_folder):
    with open(queries_file) as f:
        queries = json.loads(f.read())
    for i, query in enumerate(queries):
        output_file = Path(output_folder) / f'{i:03d}.json'
        if output_file.exists():
            continue
        print(f'Running query {i}:', query['label'])
        result = requests.get(
            query['sparql_endpoint'],
            params={'format': 'json', 'query': query['sparql_query']},
            timeout=300
        )
        if result.status_code == 200:
            data = json.loads(result.text)
            query['result'] = data
            query['n_results'] = len(data['results']['bindings'])
        else:
            query['error'] = f'Error with status code {result.status_code}'
    
        with open(output_file, 'w') as f:
            f.write(json.dumps(query))

if __name__ == '__main__':
    main()
