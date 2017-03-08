# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from eth.factories import DaemonFactory
from eth.models import Daemon
from eth.bot import Bot
from events.models import Alert
from events.factories import AlertFactory
from datetime import datetime
from django.utils import timezone
from web3 import TestRPCProvider
from json import loads


class TestDaemon(TestCase):

    def setUp(self):
        self.daemon = DaemonFactory()
        self.bot = Bot()
        self.bot.decoder.methods = {}
        self.maxDiff = None
        self.rpc = TestRPCProvider()

    def tearDown(self):
        self.rpc.server.shutdown()
        self.rpc = None

    def test_init(self):
        self.assertEquals(self.bot.last_abi_datetime, datetime.fromtimestamp(0, timezone.get_current_timezone()))

    def test_next_block(self):
        self.assertEquals(self.bot.next_block(), 0)
        self.bot.increase_block()
        self.assertEquals(self.bot.next_block(), 1)

    def test_update_abis(self):
        self.assertIsNotNone(self.bot.decoder)
        self.assertEquals(len(self.bot.decoder.methods), 0)
        self.assertEquals(self.bot.update_abis(), 0)
        self.assertEquals(len(self.bot.decoder.methods), 0)
        # No ABIs
        AlertFactory()
        self.assertEquals(self.bot.update_abis(), 5)
        self.assertEquals(len(self.bot.decoder.methods), 5)
        self.assertEquals(self.bot.update_abis(), 0)
        AlertFactory()
        self.assertEquals(self.bot.update_abis(), 5)
        self.assertEquals(self.bot.update_abis(), 0)

    def test_get_logs_wrong_block(self):
        self.assertEquals(self.bot.next_block(), 0)
        self.assertEqual(0, self.bot.web3.eth.blockNumber)
        logs = self.bot.get_next_logs()
        self.assertListEqual([], logs)
        self.bot.increase_block()
        self.assertEquals(self.bot.next_block(), 1)
        self.assertEqual(0, self.bot.web3.eth.blockNumber)
        self.assertRaises(ValueError, self.bot.get_next_logs)

    def test_get_logs(self):
        # no logs before transactions
        logs = self.bot.get_next_logs()
        self.assertListEqual([], logs)

        # create Wallet Factory contract
        abi = loads('[{"inputs": [{"type": "address", "name": ""}], "constant": true, "name": "isInstantiation", "payable": false, "outputs": [{"type": "bool", "name": ""}], "type": "function"}, {"inputs": [{"type": "address[]", "name": "_owners"}, {"type": "uint256", "name": "_required"}, {"type": "uint256", "name": "_dailyLimit"}], "constant": false, "name": "create", "payable": false, "outputs": [{"type": "address", "name": "wallet"}], "type": "function"}, {"inputs": [{"type": "address", "name": ""}, {"type": "uint256", "name": ""}], "constant": true, "name": "instantiations", "payable": false, "outputs": [{"type": "address", "name": ""}], "type": "function"}, {"inputs": [{"type": "address", "name": "creator"}], "constant": true, "name": "getInstantiationCount", "payable": false, "outputs": [{"type": "uint256", "name": ""}], "type": "function"}, {"inputs": [{"indexed": false, "type": "address[]", "name": "owners"}], "type": "event", "name": "OwnersInit", "anonymous": false}, {"inputs": [{"indexed": false, "type": "address", "name": "sender"}, {"indexed": false, "type": "address", "name": "instantiation"}], "type": "event", "name": "ContractInstantiation", "anonymous": false}]')
        bin_hex = "6060604052611963806100126000396000f3606060405260e060020a60003504632f4f3316811461003f57806353d9d9101461005f57806357183c82146101fb5780638f8384781461023e575b610002565b346100025761027060043560006020819052908152604090205460ff1681565b34610002576040805160206004803580820135838102808601850190965280855261028495929460249490939285019282918501908490808284375094965050933593505060443591505060007fe1d216d1830e177b6fd03a19f026ec2c78fc953d60bae896ab63aaa1230ff9008460405180806020018281038252838181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f1509050019250505060405180910390a18383836040516116308061033383390180806020018481526020018381526020018281038252858181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f150905001945050505050604051809103906000f080156100025790506102a081600160a060020a03808216600090815260208181526040808320805460ff19166001908117909155339094168352908390529020805491820180825590919082818380158290116102a7576000838152602090206102a79181019083015b8082111561032f57600081556001016101e7565b346100025761028460043560243560016020526000828152604090208054829081101561000257600091825260209091200154600160a060020a03169150829050565b3461000257600160a060020a036004351660009081526001602052604090205460408051918252519081900360200190f35b604080519115158252519081900360200190f35b60408051600160a060020a039092168252519081900360200190f35b9392505050565b50505060009283525060209182902001805473ffffffffffffffffffffffffffffffffffffffff19166c01000000000000000000000000848102041790556040805133600160a060020a03908116825284169281019290925280517f4fb057ad4a26ed17a57957fa69c306f11987596069b89521c511fc9a894e61619281900390910190a150565b509056606060405260405161163038038061163083398101604052805160805160a05191909201919082826000825182603282118061003a57508181115b80610043575080155b8061004c575081155b1561005657610002565b600092505b84518310156100ce576002600050600086858151811015610002576020908102909101810151600160a060020a031682528101919091526040016000205460ff16806100c45750848381518110156100025790602001906020020151600160a060020a03166000145b1561015357610002565b845160038054828255600082905290917fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b918201916020890182156101cd579160200282015b828111156101cd5782518254600160a060020a0319166c0100000000000000000000000091820291909104178255602090920191600190910190610114565b600160026000506000878681518110156100025790602001906020020151600160a060020a0316815260200190815260200160002060006101000a81548160ff02191690837f010000000000000000000000000000000000000000000000000000000000000090810204021790555060019092019161005b565b506101f39291505b80821115610213578054600160a060020a03191681556001016101d5565b505050600492909255505050600655506114199050806102176000396000f35b509056606060405236156101325760e060020a6000350463025e7c278114610180578063173825d9146101b257806320ea8d86146101df5780632f54bf6e146102135780633411c81c146102335780634bc9fdc214610260578063547415251461028357806367eeba0c146102f75780636b0c932d146103055780637065cb4814610313578063784547a71461033e5780638b51d13f1461034e5780639ace38c2146103c2578063a0e67e2b146103fd578063a8abe69a1461046e578063b5dc40c31461054d578063b77bf60014610659578063ba51a6df14610667578063c01a8c8414610693578063c6427474146106a3578063cea0862114610714578063d74f8edd1461073f578063dc8452cd1461074c578063e20056e61461075a578063ee22610b1461078a578063f059cf2b1461079a575b6107a8600034111561017e57604080513481529051600160a060020a033316917fe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c919081900360200190a25b565b34610002576107aa60043560038054829081101561000257600091825260209091200154600160a060020a0316905081565b34610002576107a8600435600030600160a060020a031633600160a060020a0316141515610a1a57610002565b34610002576107a8600435600160a060020a033390811660009081526002602052604090205460ff161515610c5f57610002565b34610002576107c660043560026020526000908152604090205460ff1681565b34610002576001602090815260043560009081526040808220909252602435815220546107c69060ff1681565b34610002576107da6007546000906201518001421115610d0f5750600654610d18565b34610002576107da6004356024356000805b600554811015610d1b578380156102be575060008181526020819052604090206003015460ff16155b806102e257508280156102e2575060008181526020819052604090206003015460ff165b156102ef57600191909101905b600101610295565b34610002576107da60065481565b34610002576107da60075481565b34610002576107a860043530600160a060020a031633600160a060020a0316141515610d2257610002565b34610002576107c6600435610801565b34610002576107da6004356000805b600354811015610e52576000838152600160205260408120600380549192918490811015610002576000918252602080832090910154600160a060020a0316835282019290925260400190205460ff16156103ba57600191909101905b60010161035d565b34610002576000602081905260043581526040902080546001820154600383015461087993600160a060020a03909316926002019060ff1684565b346100025760408051602080820183526000825260038054845181840281018401909552808552610923949283018282801561046257602002820191906000526020600020905b8154600160a060020a03168152600190910190602001808311610444575b50505050509050610d18565b34610002576109236004356024356044356064356040805160208181018352600080835283519182018452808252600554935192939192909182918059106104b35750595b9080825280602002602001820160405280156104ca575b509250600091508190505b600554811015610e58578580156104fe575060008181526020819052604090206003015460ff16155b806105225750848015610522575060008181526020819052604090206003015460ff165b156105455780838381518110156100025760209081029091010152600191909101905b6001016104d5565b34610002576109236004356040805160208181018352600080835283519182018452808252600354935192939192909182918059106105895750595b9080825280602002602001820160405280156105a0575b509250600091508190505b600354811015610ecd576000858152600160205260408120600380549192918490811015610002576000918252602080832090910154600160a060020a0316835282019290925260400190205460ff161561065157600380548290811015610002576000918252602090912001548351600160a060020a03909116908490849081101561000257600160a060020a03909216602092830290910190910152600191909101905b6001016105ab565b34610002576107da60055481565b34610002576107a86004355b30600160a060020a031633600160a060020a0316141515610f4957610002565b34610002576107a8600435610974565b3461000257604080516020600460443581810135601f81018490048402850184019095528484526107da948235946024803595606494929391909201918190840183828082843750949650505050505050600061096d848484600083600160a060020a0381161515610b6157610002565b34610002576107a860043530600160a060020a031633600160a060020a031614151561101457610002565b34610002576107da603281565b34610002576107da60045481565b34610002576107a8600435602435600030600160a060020a031633600160a060020a031614151561104f57610002565b34610002576107a86004356109f7565b34610002576107da60085481565b005b60408051600160a060020a039092168252519081900360200190f35b604080519115158252519081900360200190f35b60408051918252519081900360200190f35b600084815260208190526040902092506111c2845b600080805b600354811015610872576000848152600160205260408120600380549192918490811015610002576000918252602080832090910154600160a060020a0316835282019290925260400190205460ff161561086357600191909101905b600454821415610e4a57600192505b5050919050565b60408051600160a060020a03861681526020810185905282151560608201526080918101828152845460026000196101006001841615020190911604928201839052909160a0830190859080156109115780601f106108e657610100808354040283529160200191610911565b820191906000526020600020905b8154815290600101906020018083116108f457829003601f168201915b50509550505050505060405180910390f35b60405180806020018281038252838181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f1509050019250505060405180910390f35b905061100d815b33600160a060020a03811660009081526002602052604090205460ff161515610fb457610002565b6000858152600160208181526040808420600160a060020a0333168086529252808420805460ff1916909317909255905187927f4a504a94899432a9846e1aa406dceb1bcfd538bb839071d49d1e5e23f5be30ef91a3610ce6855b6000818152602081905260408120600301548190839060ff16156107ec57610002565b600160a060020a038216600090815260026020526040902054829060ff161515610a4357610002565b600160a060020a0383166000908152600260205260408120805460ff1916905591505b60035460001901821015610b085782600160a060020a0316600360005083815481101561000257600091825260209091200154600160a060020a03161415610b3857600380546000198101908110156100025760009182526020909120015460038054600160a060020a039092169184908110156100025760009182526020909120018054600160a060020a031916606060020a928302929092049190911790555b600380546000198101808355919082908015829011610b4357600083815260209020610b43918101908301610c0e565b600190910190610a66565b505060035460045411159150610c26905057600354610c2690610673565b60055460408051608081018252878152602080820188815282840188815260006060850181905286815280845294852084518154606060020a91820291909104600160a060020a031990911617815591516001808401919091559051805160028085018054818a5298879020999b5096989497601f9481161561010002600019011604830185900484019490939291019083901061137e57805160ff19168380011785555b506113ae9291505b80821115610c225760008155600101610c0e565b5090565b604051600160a060020a038416907f8001553a916ef2f495d26a907cc54d96ed840d7bda71e73194bf5a9df7a76b9090600090a2505050565b600082815260016020908152604080832033600160a060020a038116855292529091205483919060ff161515610cee57610002565b6000858152600160209081526040808320600160a060020a0333168085529252808320805460ff191690555187927ff6a317157440607f36269043eb55f1287a5a19ba2216afeab88cd46cbcfb88e991a35b505b50505050565b600084815260208190526040902060030154849060ff1615610c9457610002565b50600854600654035b90565b5092915050565b600160a060020a038116600090815260026020526040902054819060ff1615610d4a57610002565b81600160a060020a0381161515610d6057610002565b6003546004546001909101906032821180610d7a57508181115b80610d83575080155b80610d8c575081155b15610d9657610002565b600160a060020a0385166000908152600260205260409020805460ff19166001908117909155600380549182018082559091908281838015829011610dec57600083815260209020610dec918101908301610c0e565b50505060009283525060208220018054600160a060020a031916606060020a88810204179055604051600160a060020a038716917ff39e6e1eb0edcf53c221607b54b00cd28f3196fed0a24994dc308b8f611b682d91a25050505050565b600101610806565b50919050565b878703604051805910610e685750595b908082528060200260200182016040528015610e7f575b5093508790505b86811015610ec2578281815181101561000257906020019060200201518489830381518110156100025760209081029091010152600101610e86565b505050949350505050565b81604051805910610edb5750595b908082528060200260200182016040528015610ef2575b509350600090505b81811015610f41578281815181101561000257906020019060200201518482815181101561000257600160a060020a03909216602092830290910190910152600101610efa565b505050919050565b600354816032821180610f5b57508181115b80610f64575080155b80610f6d575081155b15610f7757610002565b60048390556040805184815290517fa3f1ee9126a074d9326c682f561767f710e927faa811f7a99829d49dc421797a9181900360200190a1505050565b6000828152602081905260409020548290600160a060020a03161515610fd957610002565b600083815260016020908152604080832033600160a060020a038116855292529091205484919060ff161561099c57610002565b9392505050565b60068190556040805182815290517fc71bdc6afaf9b1aa90a7078191d4fc1adf3bf680fca3183697df6b0dc226bca29181900360200190a150565b600160a060020a038316600090815260026020526040902054839060ff16151561107857610002565b600160a060020a038316600090815260026020526040902054839060ff16156110a057610002565b600092505b60035483101561111d5784600160a060020a0316600360005084815481101561000257600091825260209091200154600160a060020a031614156111b7578360036000508481548110156100025760009182526020909120018054600160a060020a031916606060020a928302929092049190911790555b600160a060020a03808616600081815260026020526040808220805460ff1990811690915593881682528082208054909416600117909355915190917f8001553a916ef2f495d26a907cc54d96ed840d7bda71e73194bf5a9df7a76b9091a2604051600160a060020a038516907ff39e6e1eb0edcf53c221607b54b00cd28f3196fed0a24994dc308b8f611b682d90600090a25050505050565b6001909201916110a5565b9150818061123157506002808401546000196101006001831615020116041580156112315750600183015461123190600754600090620151800142111561120d574260075560006008555b600654600854830111806112245750600854828101105b1561141057506000611414565b15610ce85760038301805460ff1916600117905581151561125b5760018301546008805490910190555b825460018085015460405160028088018054600160a060020a039096169593949093839285926000199083161561010002019091160480156112de5780601f106112b3576101008083540402835291602001916112de565b820191906000526020600020905b8154815290600101906020018083116112c157829003601f168201915b505091505060006040518083038185876185025a03f1925050501561132d5760405184907f33e13ecb54c3076d8e8bb8c2881800a4d972b792045ffae98fdf46df365fed7590600090a2610ce8565b60405184907f526441bb6c1aba3c9a4a6ca1d6545da9c2333c8c48343ef398eb858d72b7923690600090a260038301805460ff19169055811515610ce8575050600101546008805491909103905550565b82800160010185558215610c06579182015b82811115610c06578251826000505591602001919060010190611390565b5050606091909101516003909101805460ff191660f860020a9283029290920491909117905560058054600101905560405182907fc0ba8fe4b176c1714197d43b9cc6bcf797a4a7461c5fe8d0ef6e184ae7601e5190600090a2509392505050565b5060015b91905056"
        factory = self.bot.web3.eth.contract(abi, bytecode=bin_hex)
        self.assertIsNotNone(factory)
        txHash = factory.deploy()
        self.assertIsNotNone(txHash)
        receipt = self.bot.web3.eth.getTransactionReceipt(txHash)
        self.assertIsNotNone(receipt)
        self.assertIsNotNone(receipt.get('contractAddress'))
        factory_address = receipt[u'contractAddress']

        logs = self.bot.get_next_logs()
        self.assertListEqual([], logs)

        # send deploy function, will trigger two events
        self.bot.decoder.add_abi(abi)
        factory_instance = self.bot.web3.eth.contract(abi, factory_address)
        owners = self.bot.web3.eth.accounts[0:2]
        required_confirmations = 1
        daily_limit = 0
        txHash = factory_instance.transact().create(owners, required_confirmations, daily_limit)
        receipt = self.bot.web3.eth.getTransactionReceipt(txHash)
        self.assertIsNotNone(receipt)
        self.bot.increase_block()
        logs = self.bot.get_next_logs()
        self.assertEqual(2, len(logs))
        self.assertDictEqual(
            {
                u'address': factory_address,
                u'name': u'OwnersInit',
                u'params': [
                    {
                        u'name': u'owners',
                        u'value': self.bot.web3.eth.accounts[0:2]
                    }
                ]
            },
            logs[0]
        )
        self.assertDictEqual(
            {
                u'address': factory_address,
                u'name': u'ContractInstantiation',
                u'params': [
                    {
                        u'name': 'sender',
                        u'value': self.bot.web3.eth.coinbase
                    },
                    {
                        u'name': 'instantiation',
                        u'value': logs[1][u'params'][1][u'value']
                    }
                ]
            },
            logs[1]
        )