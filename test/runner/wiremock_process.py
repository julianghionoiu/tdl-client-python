import json
import unirest


class WiremockProcess:

    def __init__(self, hostname, port):
        self._base_url = 'http://{}:{}'.format(hostname, port)

    def create_new_mapping(self, config):
        request = {
            'request': {
                'urlPattern': config.get('endpointMatches'),
                'url': config.get('endpointEquals'),
                'method': config.get('method')
            },
            'response': {
                'body': config.get('responseBody').replace('\\n', '\n'),
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

        unirest.post('{}/__admin/mappings/new'.format(self._base_url),
                     headers={'Accept': 'application/json'},
                     params=json.dumps(request))

    def reset(self):
        unirest.post('{}/__admin/reset'.format(self._base_url))

    def verify_endpoint_was_hit(self, endpoint, method_type, body):
        return self.count_requests_with_endpoint(endpoint, method_type, body) == 1

    def count_requests_with_endpoint(self, endpoint, verb, body):
        request = {
            'url': endpoint,
            'method': verb
        }

        if body:
            request['bodyPatterns'] = [{'equalTo': body}]

        response = unirest.post('{}/__admin/requests/count'.format(self._base_url),
                                headers={'Accept': 'application/json'},
                                params=json.dumps(request))

        return response.body['count']
