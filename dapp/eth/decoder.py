from ethereum.utils import sha3


class Singleton(object):
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not isinstance(cls._instance, cls):
        cls._instance = object.__new__(cls, *args, **kwargs)
    return cls._instance


class Decoder(Singleton):

    methods = {}

    def add_abi(self, abis):
        for item in abis:
            if item[u'name']:
                # Generate methodID and link it with the abi
                method_header = "{}({})".format(item[u'name'],
                                                ','.join(map(lambda input: input[u'type'], item[u'inputs'])))
                method_id = sha3(method_header).encode('hex')
                self.methods[method_id] = item

    def remove_abi(self, abis):
        for item in abis:
            if item[u'name']:
                # Generate methodID and link it with the abi
                method_header = "{}({})".format(item[u'name'],
                                                ','.join(map(lambda input: input[u'type'], item[u'inputs'])))
                method_id = sha3(method_header).encode('hex')
                if self.methods.get(method_id):
                    del self.methods[method_id]

    def decode_logs(self, logs):
        decoded = []

        for log in logs:
            method_id = log[u'topics'][0][2:]
            if self.methods.get(method_id):
                method = self.methods[method_id]
                decoded_params = []
                data_i = 2
                topics_i = 1
                for param in method[u'inputs']:
                    decoded_p = {
                        'name': param[u'name']
                    }

                    if param[u'indexed']:
                        decoded_p['value'] = param[u'topics'][topics_i]
                        topics_i += 1
                    else:
                        data_end_index = data_i + 64
                        decoded_p['value'] = "0x" + log[u'data'][data_i:data_end_index]
                        data_i = data_end_index

                    if param[u'type'] == u'address':
                        decoded_p['value'] = hex(int(decoded_p['value'], 16))
                    elif param[u'type'] in [u'uint256', u'uint8', u'int']:
                        decoded_p['value'] = int(decoded_p['value'], 16)

                    decoded_params.append(decoded_p)
                decoded.append({
                    'params': decoded_params,
                    'name': method[u'name'],
                    'address': log[u'address']
                })

        return decoded