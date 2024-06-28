import json
import requests


class WiremockProcess:

    def __init__(self, hostname, port):
        self._base_url = 'http://{}:{}'.format(hostname, port)

    def create_new_mapping(self, config):
        body = config.get('responseBody')
        if body:
            body = body.replace('\\n', '\n')

        request = {
            'request': {
                'urlPattern': config.get('endpointMatches'),
                'url': config.get('endpointEquals'),
                'method': config.get('method')
            },
            'response': {
                'body': body,
                'statusMessage': config.get('statusMessage'),
                'status': config.get('status')
            }
        }

        accept_header = config.get('acceptHeader')
        if accept_header:
            request['request']['headers'] = {
                'accept': {
                    'contains': accept_header
                }
            }

        requests.post('{}/__admin/mappings'.format(self._base_url), headers={'Accept': 'application/json'},
                             data=json.dumps(request))

    def reset(self):
        requests.post('{}/__admin/reset'.format(self._base_url))

    def verify_endpoint_was_hit(self, endpoint, method_type, body):
        return self.count_requests_with_endpoint(endpoint, method_type, body) == 1

    def count_requests_with_endpoint(self, endpoint, verb, body):
        request = {
            'url': endpoint,
            'method': verb
        }

        if body:
            request['bodyPatterns'] = [{'equalTo': body}]

        response = requests.post('{}/__admin/requests/count'.format(self._base_url),
                                 headers={'Accept': 'application/json'},
                                 data=json.dumps(request))

        content = response.json()

        return content['count']
