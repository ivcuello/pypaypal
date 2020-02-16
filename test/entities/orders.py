"""test module for pypaypal.entities.orders
"""

import unittest

from pypaypal.entities import orders


class TypedPhoneTest(unittest.TestCase):
    """Test class for TypedPhone"""

    def setUp(self):
        self.sample_dict = {'phone_type': '58044B279649DD68161520B4F53470EA2CDA97B5A0BFECD8E8BA9A8D40EDD347', 'phone_number': {'national_number': '21D592F9E0034BD1F8CAFDCE5876AD78E36AB9E5B747AC9AB3106D58EED922C4'}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.TypedPhone.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.TypedPhone.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class TaxInfoTest(unittest.TestCase):
    """Test class for TaxInfo"""

    def setUp(self):
        self.sample_dict = {'tax_id': 'CF8CC0E52536C3346B560675D61896FA50044EE6B3E833A6369263FD696784B8', 'tax_id_type': 'ECBA3FFEDC3E86556DCE96628BE9C3027159E94EDEF1172D716CE1EDF543D443'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.TaxInfo.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.TaxInfo.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class PayerTest(unittest.TestCase):
    """Test class for Payer"""

    def setUp(self):
        self.sample_dict = {'payer_id': 'D8F86BA193EF496B506CE00DFCD62256DE3839791D46A644C4C9FE3509210EFC', 'name': {'surname': '65F243C10A7455898BF44B653AFBC614144B1128CF89535220481A8BE8C42485', 'given_name': '753B265EABB53A64255CF9DED7DE8A4D615F30FA0DB62305AC47BFA7F8090A29'}, 'email_address': '3EFEB21E7936287D1771BD09950421F16FB54050700285FF5C652BB7F8AEAE5D', 'phone': {'phone_type': '3748A42091E307835FBD6725353E5E60A9342F15137C34EF73D8678DC63AF2EC', 'phone_number': {'national_number': '2FA15042383FEFCFD44D030C8A248B2C93F18B73BB02A514BB1B69D43C8A72B6'}}, 'tax_info': {'tax_id': '0B34428AD38E6B536BD7C774F2DF8D521A0E3D32442BF66120B2F1C1B2AF62B4', 'tax_id_type': '05A90D4E088203727B551457AFB904AB16E844FA583FA01EE3F20F41BA36257A'}, 'address': {'postal_code': 'AA706A14D3789D716D5865432523066E6B52D8453B55DE19A8F72D95E767D686', 'country_code': '7A0D753DAA9C6058B9BF92536A34163FE97F1E8F2C158609972DBB58B5C41E75'}, 'birth_date': 'D62878F9F1600576F9CF0ECDA3FE5D54697FACFC54EA7E179721BE49B7FC73EA'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.Payer.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.Payer.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class AmountBreakdownTest(unittest.TestCase):
    """Test class for AmountBreakdown"""

    def setUp(self):
        self.sample_dict = {'item_total': {'value': '39B129B339E8B342B43032BFB15E1E3FF88B1CB97D081E210824DD4AE6E3A9B2', 'currency_code': 'USD'}, 'shipping': {'value': '83AE9E7F7372BF955059A2031D2D4A6C7CFEE943ACD8B65304FBB70508BDD5FD', 'currency_code': 'USD'}, 'handling': {'value': 'E088AA935A1C338076F537EF00E9B4563AD61F2BEFD7111194003028ECE71B73', 'currency_code': 'USD'}, 'tax_total': {'value': '48C36BF50F7B53B1621BFFBD075355156D21DE7AC2F2B2704D195EF5D87A11BD', 'currency_code': 'USD'}, 'insurance': {'value': '58648779E11E3024FCB19E124F937825160B64AEE378DAE7942D177E8D51B725', 'currency_code': 'USD'}, 'shipping_discount': {'value': 'FEC41599AA0B4F22B5542D6FCC3813B1812085334E9DA9E42A6F5AE946EF9179', 'currency_code': 'USD'}, 'discount': {'value': 'C5C19D16965D9A3D557FFB020758BE251C94D89CB21754528BFAC8C3B644FA4E', 'currency_code': 'USD'}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.AmountBreakdown.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.AmountBreakdown.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class AmountWithBreakdownTest(unittest.TestCase):
    """Test class for AmountWithBreakdown"""

    def setUp(self):
        self.sample_dict = {'currency_code': 'USD', 'value': '10FEC96E793BB351A17DBAAFA67FFBD2F1CE453902165DE66F8FC78B76508AF5', 'breakdown': {'item_total': {'value': 'FAFBA2B0E190B7926CE64BD7BE7C584DBD031CFCAB4C58316FCCB5E972CA8D4F', 'currency_code': 'USD'}, 'shipping': {'value': '3FAD78F4355CB9378637B996188C35D411741936EF9262609FEFD3F7DA2A02C2', 'currency_code': 'USD'}, 'handling': {'value': '09B2269DAA7910A185F32B9C1D912421D12313A269877FB789637EB7E194B71A', 'currency_code': 'USD'}, 'tax_total': {'value': '472B99B21875D600849110CB8D340F3F80EA14A2B2C53AA6C71982E6CE7AA160', 'currency_code': 'USD'}, 'insurance': {'value': 'FDDC90064406F3D188E7A7F06C2D53A08525F538DFD1FD7C3C663EFE5853D625', 'currency_code': 'USD'}, 'shipping_discount': {'value': '0A5823384D480623A8A0D355E69A95B7FC57DCBB2E42985C9A17FE2F7D977D74', 'currency_code': 'USD'}, 'discount': {'value': '1BD97D6893DAE379B23C149C26540ED0750D48A0E7F211750AFBF94B126AF492', 'currency_code': 'USD'}}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.AmountWithBreakdown.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.AmountWithBreakdown.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class ItemTest(unittest.TestCase):
    """Test class for Item"""

    def setUp(self):
        self.sample_dict = {'name': '5454146367D2B9B69411C95CD6DBA482B15116314F21808F22D3696E7AB10A86', 'unit_amount': {'value': '4B8E20338EFF218CBF3D1F0F836B7DD310DD11CEFC970E060673524CE0AB0858', 'currency_code': 'USD'}, 'tax': {'value': '7CA293CFC64A832D178BA7CEA79E9B53CC8C423AE6318F7690CF1163E3C7F932', 'currency_code': 'USD'}, 'quantity': 'B5E7CDDDA09CB424FABABC39DC68632FC55FD0AD77925C4E4C6E055926897E93', 'category': 'B8C6E9E648C4EF101B1B05EB13EED519E44B9A6F2CE9566D0D68172EE8C2C3F2', 'description': '6CDC9F68DECD0C3C758F6B708665FC523F19B201D9148CA1832716EA162B63D7', 'sku': '0609AD3B5D42737C32BA0AB5348A4E8AEBC49DD7D9FCB15220B4C7A89337D6F4'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.Item.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.Item.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class NameTest(unittest.TestCase):
    """Test class for Name"""

    def setUp(self):
        self.sample_dict = {'full_name': 'CA979034C41887C4486CB0472B5FA75B4E50C88C6BD0C93704CDBC53CFAB83E8'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.Name.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.Name.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class ShippingDetailTest(unittest.TestCase):
    """Test class for ShippingDetail"""

    def setUp(self):
        self.sample_dict = {'name': {'full_name': '3B81790A8A4A0B8786AB03A7269CA4F7C5D4F40BF047D613F60B108B5DB9A772'}, 'address': {'postal_code': 'FE296FF23F5DB8FBAB6AAC0E211F231B70B15AF4F36A9626BAE07A907DCA99A5', 'country_code': '2495CC03D10845F8FD4173D0B1A625827B9EFAFF349AF9E7DDC278A68B3BD02D'}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.ShippingDetail.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.ShippingDetail.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class OrderPaymentTest(unittest.TestCase):
    """Test class for OrderPayment"""

    def setUp(self):
        self.sample_dict = {'captures': [{'id': 'C7B555B11CD0B8F53EAAF75CCA73580D2BAF059057D2A188EC80B8A64453FB00', 'status': '5D4857A9A90765A40B369107ED7FE34D2720C3EAB44740900588A2E073CBA713', 'disbursement_mode': '79F3B73022CCAC17A2E588C97F21F151420FD957A1173E96F95238EF7BD1AB4D', 'invoice_id': '2E1ACBF44301C9D4F28B7C2985D1C22532DE8A675887F25C790D3522BD7F8BBC', 'custom_id': 'D92D9B5E79A7725B08FF9B41B5E5DFC9179A647793EA168170EF892CA92CA09B', 'amount': {'value': 'FBC37BCED2F0CDBE528B9683ADE26F76D422A8D412D4684A02F6538EE3D2EC0A', 'currency_code': 'USD'}, 'seller_protection': {'status': '86F85E6BD3602F296150A8B2789FE8073F51934B0CB1F59241A3294F3B26259E', 'dispute_categories': [{'dispute_category': '16BEF27F7998B30DFCF96B612F73C187A631E7458C5165529499F7186F65E9E5'}]}, 'status_details': {'reason': 'A521BED3ED6EDF21DEE339213FE71BFF24CD8A9A2B04500CF8940CAD2DD58445'}, 'seller_receivable_breakdown': {'gross_amount': {'value': 'FCA1ACA7C1CC49F967D4BA5414A2A463297EAEC91A3B12B3C0C0B80A8A8466B3', 'currency_code': 'USD'}, 'paypal_fee': {'value': '0DC911EE19F66958FE7C7595C0155A560C3EA996BA149ED835E196247173E83C', 'currency_code': 'USD'}, 'net_amount': {'value': '42EFCC7022C4ED406EF746245F3C9AA810B0E28CA0B1174DFEF8DC6A7DF2B8C9', 'currency_code': 'USD'}, 'receivable_amount': {'value': 'DCE17651A478659E2981C668EF37F7C5F300A799297F33036A737E59E16CEC82', 'currency_code': 'USD'}, 'exchange_rate': {'value': '93A78D2E9EAAEBFEC343A7D8CFB145CA54AF6DAFAC84EC1CF30E84FEBE7A38E7', 'source_currency': '03CEF84F88D1159F0A93FB1C56B90AFB315B34154719072D73341741631F9752', 'target_currency': '4247EF186FE3B0571016F1CCFC2D1ED84967AF51950EBF9EDE1307E60E5659DC'}, 'platform_fees': [{'payee': {'email_address': '433DE7AD9875B77BD8E60C23B8F3E4F309C5A3F389447F11F070AE8E7B965939', 'merchant_id': 'E9AB897E7592A1EB9B33D4B80293BF6A95209CCCFE6641E6D96A590C0C593AB4'}, 'amount': {'value': '3BAD6C3FE1D502287E61278E837A46C2B1D0F3DDE6132C424DD306124ACBE247', 'currency_code': 'USD'}}]}, 'links': []}], 'authorizations': [{'id': '7578704108043473D3858E0D7256FDB116D4D3B0856AE4775C07A8A66EDD854F', 'status': 'EA5597DB8F18B07B4C73114E214E1824992992E246147BF411DF7BD0C2A5E91B', 'amount': {'value': 'A3DAD50B02463B304FB30B9CB26709367D1906E9A77222268F68D4A4DBBE8F11', 'currency_code': 'USD'}, 'status_details': {'reason': 'AAEF858AD1AE490BC274E78D5B6C3CE67BC2823962AA25B530D82B57D47BF972'}, 'invoice_id': 'AA6B7C8A291FC6D67EFF5FC22D599930D2C9F5FCB924AA1B465C7D0038487E84', 'custom_id': 'EF3747AD72CC156BE537FD6F04C0EF535EBE400378501E7481C0C94FF06B63AB', 'seller_protection': {'status': 'F2418D33167510B0C2E902D20B8E5FBCA60FA54C2495984EC4627FFAE95A7D5E', 'dispute_categories': [{'dispute_category': 'F3472A31B0F982D2ACC09FD387E3A72163CDBB755C5E6E66C13BD77E17024AF1'}]}, 'links': []}]}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.OrderPayment.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.OrderPayment.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class PurchaseUnitRequestTest(unittest.TestCase):
    """Test class for PurchaseUnitRequest"""

    def setUp(self):
        self.sample_dict = {'reference_id': '4E7C51BA562605A1FA85FF099965C4C6DDF2DECEBCDB11E8B85D2A6CF8FA49BB', 'amount': {'currency_code': 'USD', 'value': 'E60E50C3CCFBEDFB46D6D64038434BCB47F63E3E75ED6296EFE7C88DEA3658DC', 'breakdown': {'item_total': {'value': '76DBBAAF5375CB53485BDD1B4DB1AFC68CAC38003BE3B546A60641ADA1FB4136', 'currency_code': 'USD'}, 'shipping': {'value': '89970C213D44F57EFAFABA93782999317D6119EA59C9227BDD18291614AE5969', 'currency_code': 'USD'}, 'handling': {'value': 'B11835D55F5181052628167EF058FDF984AC3FC4003A573FCD652C2E24DF19C2', 'currency_code': 'USD'}, 'tax_total': {'value': '7447BA8EF1BF52F1337295F3E0927C79B34611F3AD8483D2E2B886142E615070', 'currency_code': 'USD'}, 'insurance': {'value': 'B391C9D008F651FCA55084065C960D5A8D02C4FF9DAE32E6B9637AFCF424836B', 'currency_code': 'USD'}, 'shipping_discount': {'value': 'CA04E57CC1A5234E820866F51DBD5886633B605060240179C7E5394F4A748C73', 'currency_code': 'USD'}, 'discount': {'value': 'E8895E710247F7AF55D966DBCB756CEE296EE612CE4F38CA71C51B734C1D6DA8', 'currency_code': 'USD'}}}, 'payee': {'email_address': '42EC792CB946C36ED28ED2E270AA2C42D3CB215C065815ED611500F45B55C666', 'merchant_id': '713A9A36A57917108F1C103B46F4BC059E1165BF136DE861621F60E8CDB53CC3'}, 'payments': {'captures': [{'id': '26FB83C899113BE6E8B3A47528DBFDB6EC27644D35EA592E1E888DC71D912B62', 'status': 'C226D5F7CEB86D3187627AB12DEA072EDB82CDACDBC7040829039FA59238F2AC', 'disbursement_mode': '3BCF5893BD231BE1540FC1A409A258EAAA8C8DFB4AB5CDEB4891BAEF63B0AFF8', 'invoice_id': '5583CF600698E37BC31BBB92D45614D1DDEBCDDAB1AB3B6CECDD9C430D33A62B', 'custom_id': '38ADBAE7B029BD8FDFC1277EB437D086F7FF8D512DFD3CCA6AEF433A054EC13C', 'amount': {'value': 'A17835F8B065D0AD8CD84A7513CC01C8A6EF9D01603FD273E87E8F17F3C5A2B3', 'currency_code': 'USD'}, 'seller_protection': {'status': '89926F418812FA0844EFDF46A702A0B1F2066AF6E2E62A1C1BD8AB961CB0EA81', 'dispute_categories': [{'dispute_category': 'DBC39B7778A322253AFA71DBB0276A17A5E35809D9E7EF199905F8EB4CFB274D'}]}, 'status_details': {'reason': 'EE00F688F17AF85A48EAD4035CAF74A2D504B7C3B74E669715215EAF383E38DB'}, 'seller_receivable_breakdown': {'gross_amount': {'value': '87B06C74F95DB2BFAF1522CEFC9823D8EDB4A6E04B150364EE85B5F3A261CB67', 'currency_code': 'USD'}, 'paypal_fee': {'value': 'CFFB3096FAE4C6A2E9E6499B215EC778D72C1E004EDEF886559D0CD136AF8985', 'currency_code': 'USD'}, 'net_amount': {'value': '6B0C10E6725C8D60ED08E998FCC3691AB967A51B23320FD158834CCE5784B594', 'currency_code': 'USD'}, 'receivable_amount': {'value': 'A390D2C08366FD4344D26608AD873EE8556D8D56F0875CC747A805FB2CCAB558', 'currency_code': 'USD'}, 'exchange_rate': {'value': 'DAB58FCE2961E38B2F6861A11C60AEC211AD7399CF8FC8844FF8FBFA0D0EB71B', 'source_currency': 'E25F91803EA9FFAD6BF48B5CE515BEF7DB27F8DA306138D9D23A3688BBA88B1C', 'target_currency': '97F740234BF21DA0D69FBA1E5B0F8F6A85DEC10A729CA5B82C7606F3AF6B6F9F'}, 'platform_fees': [{'payee': {'email_address': '830A35EE2CD102F44C8D50F3720E1580A6D61D362EAEDD3B42C87DA7CAA286F1', 'merchant_id': '47690FCF4C8D39FB8247578B77BA405D0370027628F3DE2424F41BBB6A36DE42'}, 'amount': {'value': 'BA2E6923031BB86F34E74FC713B86CCB7D4F20271A4F056A88EEC20A9CAD36A3', 'currency_code': 'USD'}}]}, 'links': []}], 'authorizations': [{'id': '75EA2F908C90FEE355AFE6E2CF9AC7DCA1F2CC32C008ED9CE9C59A90B64F7B8C', 'status': 'D7DD2DBFCF7AFEDBBA02E2BAF5F4D2548FD75672F26393AEF6936E1B46858CC2', 'amount': {'value': '8ACC8AA791CEA0256D2127584A3D07418AB96F62AAF5D2BEF5F44DA9BD339D7C', 'currency_code': 'USD'}, 'status_details': {'reason': 'F43FB7C1AB43FCA4E566C170A5846934712627AC7758694F43A954746394D59D'}, 'invoice_id': 'A81E05E637F900FFFA50BB71314D0E7F0879D83C2BD091E31145E5917B31C929', 'custom_id': '648C88075E5106F2FE89B19DCD02D8ED455D0EE9D8F603A98031ECC1AFE9E215', 'seller_protection': {'status': 'EB4D3AA102EE3A530DB0A787E7E5A86AC0A8C5CF815A8BF05743CF4FF5AE5DBB', 'dispute_categories': [{'dispute_category': '26441305D0936B88ECE48AC9D8F4B6E733F3DD74BAE89389CACF39E07094C7BF'}]}, 'links': []}]}, 'payment_instruction': {'platform_fees': [{'payee': {'email_address': '3DF562B50BFF3618243E540DF7A821D35025114EFA12109A4B8205A0AF8A2B9B', 'merchant_id': '34FD09758577E1A4A5CAA1339440D498E863F82E836C61E400AA779EAB30D381'}, 'amount': {'value': '00BFF11BA7FD284309051844F8D22DA6DF820236FFF4086666B87D72B181EDE9', 'currency_code': 'USD'}}], 'disbursement_mode': '3F611E4B05E274B6D992A00006A6F9FCADCA01FC5FAC68C58DD59B676FE424DD'}, 'description': 'E9656A01A0404C036EA6E0637A737E44FA6A13E2B3534A19530B8546CCA4A53F', 'custom_id': 'CC9282B57805506EB00737831A97A8525021D5578C5DD2C1A8ED00F24545F1C2', 'invoice_id': '0AAA16538841E679DF1CDF37C64EC34B368F710D4E67750CF8FD0661D3AF895D', 'id': 'C723CE012724BA3386CFCFB5FE96831ACDC26CBD5B6CFD02966928011DC11C25', 'soft_descriptor': '8BD5320209BE0B8B42911E7C8FE501173FBB2F8C3D126086351D503F8FFBD457', 'items': [{'name': '569E8C5D7DE0CA49F2A8D21406E776237E29DFDE7221AC05E2D4410355D40978', 'unit_amount': {'value': '54BA7B67B79E311E77125451DCE689046E95F9D118D89151D44B1EDFF2614770', 'currency_code': 'USD'}, 'tax': {'value': '58703DBCC93CEDEAA15EBCF23F62DBA469FE6957D599543575A0BBFF1CC04875', 'currency_code': 'USD'}, 'quantity': '2B8034E44649E0847509919A818962A8A39A58CEC512F3AFCA333B25AE0044E1', 'category': '3A4BF8D75A3F908319E83DD7C37A1CF4D0A0F0DD3EE5BD5F1E9C515E09897C17', 'description': '1E7BAC399C9D64DD9096EB2F264BE33F9F4741C22AE5C5D6C79297A9D6812733', 'sku': 'B52DD7B21DF83C1994CBBAE7E293AF8DEF2D1D4B6A6C194FB5023196B76A9131'}], 'shipping': {'name': {'full_name': 'D196C975BAE6EBF0463968E384CCC212EA1130D15856F499F8DE73688B6C53E6'}, 'address': {'postal_code': 'AE8DB9ABE69A8C3EAEC34449047B6F93DCE69ABFCA9C935E634AA2199D1C191C', 'country_code': '1C1A8A768C194273AF7A40E259AF281027BED9EEBAE8822AB69B40BB36E19E27'}}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.PurchaseUnitRequest.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.PurchaseUnitRequest.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class OrderTest(unittest.TestCase):
    """Test class for Order"""

    def setUp(self):
        self.sample_dict = {'intent': '7C984045F6A3AB84F818A6E1B0ECC58928A32B6FB78A1FEAC08A19D15D5F0EA8', 'payer': {'payer_id': '453BD73E990A3D82FAC92253C5F6FD357B6D598788391219A58EBB138DDB2C3F', 'name': {'surname': 'CE241E1D05C1B5DDD9BB0B269D471F6FEF1F3B55429273D951C43E277A7DBA07', 'given_name': 'E8253C3241808635EB5FAC4767AF233794AF1B4A0C195F87DC51C3086979005F'}, 'email_address': '9F36CA332C59F1E4297816EB3DA6C5BFCB3FD8A8B7C29CE0DBF81C66461951E5', 'phone': {'phone_type': '680003BE65579E4D2C689D6F31ACAAD4843B2EE414BC7AD0AE44D59855661B17', 'phone_number': {'national_number': 'B73A08CEFBCA124AB749C8BE20A80DD5E2693CFCAFF86E07717456BEDFB4531C'}}, 'tax_info': {'tax_id': '0652DF217C775572E3C4AE563D9B3D90D3884982D7584D487BD6990F9DB6B3A0', 'tax_id_type': '228DAD80F9A5348556063DD31BB9548F364F7DC7B4F523835F384F7B50128675'}, 'address': {'postal_code': '489ED911CD81A55CBA31DF2EC6CA5C8283036FD1A866C0EF5C2435F73F810799', 'country_code': '789A9F1D504EEFC8ABF7ABE179919E4D5E75FBB940316E62278930FB18FB32AB'}, 'birth_date': 'E9D951CC927576DE4FAFDDFF4C531514FF8FADD827671E5BCFC2F11BE2CFD465'}, 'purchase_units': [{'reference_id': 'BC8B2C37F95C4FACAFFEDC166DB2BCB7DA9FDF819124306C6D2364648D541AEB', 'amount': {'currency_code': 'USD', 'value': 'B4B22FFCB562F900FDCA9837B4CBE257022B198C877F1B47ED0FC4E099CD2080', 'breakdown': {'item_total': {'value': 'FED05215FB39F5F6FCD44A4A2B3F0640E90A9CAC27D88E4FA68768181DB18DB4', 'currency_code': 'USD'}, 'shipping': {'value': '5FBFE527BC320E51E8742E50326FC4ECEB39F25F5F290529792CF02FD02336C2', 'currency_code': 'USD'}, 'handling': {'value': 'F6682D3636FB04A6040AE84A2B529C00507F48A491DD11CA89C2C5C32920DCE0', 'currency_code': 'USD'}, 'tax_total': {'value': '31A2E50958EA01FF23C1EA1FA70E3AEED7A6F19A3E25FE2CA19E0D33F7F9AA6B', 'currency_code': 'USD'}, 'insurance': {'value': '8ABA14628D472E8BF14916FFFC6D5EB99BB6F648A6E3A34227126A17AA1E885B', 'currency_code': 'USD'}, 'shipping_discount': {'value': '3F4CB7A974B8032838C9BBA8F7F615D087AC2FBE81F5168F9D1E131F8D5410EE', 'currency_code': 'USD'}, 'discount': {'value': '30117D4D3665715DC639AEB73A625B05BC0057F6EAE2EC98738C849652CF606C', 'currency_code': 'USD'}}}, 'payee': {'email_address': '4BCF4A58A3F06014A6F48BD175C70939C451EE31EDA7F41F8479BA3614D3EF29', 'merchant_id': '306FBF8617094C9A0BBA6E732BE789C9AFC07BADF84F5BAF9BD6B2FBF191F840'}, 'payments': {'captures': [{'id': '0030910DAB484619050F4B1A39DF68C97B95774B44BDB91012451FB648E62283', 'status': '2108EA32D41F5FBD733316A2AD4252C7535D701EF5C251E7B48E9EDDFC20058C', 'disbursement_mode': 'BD95D243E9477567F0870E5F98BE71B176E5D4707E11ED2152F17B72CBD0B314', 'invoice_id': '6D303A6924316476B98059F519E01ABF7BB4EE483710C8AE5CE73696EFE796B7', 'custom_id': 'F461A037755D0BCA91A67142C5B712E3AA8B70D46FEA6C30F923654EC4B5DBEC', 'amount': {'value': '847FC70D47EEA47645B55A58DBB702EBE7629431719345EEA79427D83AAAFBEC', 'currency_code': 'USD'}, 'seller_protection': {'status': 'B3795279FA27E6C37B7CAD9AD587CD80CBC8117D5ECD5DE3BCCF1D2E11277E85', 'dispute_categories': [{'dispute_category': 'FE322B63FAA5D7887F4FC32C2A7C1962AB48580442E0588F1D4A3A1528A75560'}]}, 'status_details': {'reason': '88DE9334163D456CBB92E4CEF21230C92FE0B041C4233FC5C67E2A0221B36FCF'}, 'seller_receivable_breakdown': {'gross_amount': {'value': 'A1F1E0D6BEA4968F4CCDC91B6A7E57DF4CC2BBB62780D54651A02B493EB32B9E', 'currency_code': 'USD'}, 'paypal_fee': {'value': '912492C466EE471A1D0F0A2B245578A04961CAAA87BF1D2A0A43BEADED1B04A6', 'currency_code': 'USD'}, 'net_amount': {'value': '4A367D994258EC05343A8E2CDC1EE10C70D221472D38A410C749D18B2EA9A0E3', 'currency_code': 'USD'}, 'receivable_amount': {'value': 'D8BA8B65D4720C41B689E59EC02C00B165BECBFE31E17558762392D6FDEA2074', 'currency_code': 'USD'}, 'exchange_rate': {'value': 'C12B7B227F5884D90CBCA1D2BFF81DDFF2F3C28CCE1F5A1FC0BA91C80CE1E479', 'source_currency': 'B287D4B592069C13C8D04BA16E4AB8BDAD12A7113DFB82419703815E040DC932', 'target_currency': 'A9BC339D4856CA498FC2B108EB945720C42384392A7363E25A07848883B7C12D'}, 'platform_fees': [{'payee': {'email_address': '8E82B845B62E6BB3BE96CA1E3B57899E88A462B15767A73B5DE4E344D76FCDAA', 'merchant_id': 'C9E5B0BAD5578BBE08648795516756325FF33B6F2E85D2B1B4C6AE223F622C90'}, 'amount': {'value': '920C5E62C37F0ADB05967E1EB89E8702392DF6AB8DFEC2C419B6701E05A9FF69', 'currency_code': 'USD'}}]}, 'links': []}], 'authorizations': [{'id': '81B4A766182F436669E92B4062EA86D5313373BFB769C05E012045D51F361327', 'status': '79A3F08658444C1ED846E39F771C7400D2677A7EC9E210EB20F79C9C862E6AD8', 'amount': {'value': '8E4274619037FFE8CA705AD66CB1CD7A9302350C5D67F10CAE9B44E1E7927A71', 'currency_code': 'USD'}, 'status_details': {'reason': 'B31515DF62BC696DA856805ED85B29A7C1787464F9EA3234D95A174DD2C6BD7D'}, 'invoice_id': '6F602FF0E6FDBCF0028710C3E78DFD5051336794277C136A8C4FD2C66E0301DF', 'custom_id': 'EE8B64DAD3B4294D7F84F74779FFCC7CE0C26011281EB56597B58FC92CED3FFE', 'seller_protection': {'status': 'F0FF93E052F84D07B70FDE99E1C92F1D3889927272BD2E42F897C38D373C6765', 'dispute_categories': [{'dispute_category': '23C2AC62DC301E2E2E5198A91EA7E0390DCDE3719A2CE2F8D27E0ADF90C0272D'}]}, 'links': []}]}, 'payment_instruction': {'platform_fees': [{'payee': {'email_address': '42A9039318D0E4BEF8AEAE0ECF4775261CFC9C0A6355DEF3D88E1667CB51E5CF', 'merchant_id': '8E18A16F2C1D5392BE71211860023B0A674DA2889E7C2368B74903F862B16DE1'}, 'amount': {'value': 'F5ACB2D7E486D91DDDC594E1787E730AEAD5D8D214642E986E0900D172F9C69F', 'currency_code': 'USD'}}], 'disbursement_mode': '0DD00585FDBFE7DFF6718007512C184A8641495867C8B21F8E88C68625F83549'}, 'description': 'FA41A2352645A5101FF94C21EF76D41119F071AD6B27D73B6B062F8AEC0A43AB', 'custom_id': '76271E933FBE349DCD2E8514998B9ADE6645B02F83EDF9B914A0230A15B342F6', 'invoice_id': '69CB7A2B1BA6E4BFA8ED79979FDC0EC72092D6CDCEF85FACE9B7E3AD3F25E9C8', 'id': 'D03ABDEF4F9229A7A904911062265C5C745CC96986A96DADBF1F234A8F0F093A', 'soft_descriptor': '41E8C0B04E5E6BC7D1E6448E3B636E98C4364C1EB61E8DBC5F47E2DF3CA3881E', 'items': [{'name': 'B973C5928314D2057ACBCD236CBBF96780E04721A412AAD2F04E430548AA4FAB', 'unit_amount': {'value': 'E014EE6FF67B45FAED33966E8E2892E98D48659B780C774EEE9E299663B1DFC9', 'currency_code': 'USD'}, 'tax': {'value': '595442A12E1C526376F1DBE1CF250E3711A6A29B81EF16A7C13D058225FD69C9', 'currency_code': 'USD'}, 'quantity': 'CDA7A843F5758B4F08978C34FA04ED0FB097392F8CDCBB33D340995DCD5F9AA7', 'category': '1467A126171B9BE76F4ECC9B2C0A74028BA4A4834D9D3742D37689A101981D13', 'description': 'C46CDA6E906F4539669C314709BE56DC79309F32EA28E644D7B75FC7C1B230ED', 'sku': 'A0C2855CDEF12C9A29FF96274BD0B0115D16CAA5D55BC08CCF7E557A7C956728'}], 'shipping': {'name': {'full_name': '6BD54BE7BE6328EFA64C04D9BAA00343C9775A902E587963C7EBF8C00CB7D4EF'}, 'address': {'postal_code': '522F573355E2E480C00EEFE4844BA356F39EF0DD662B20B117F05B6016B11838', 'country_code': 'F1515E6E859E14C29D93CDCF5AFD5038EBBEFEA89DE23B78FE9898D406C94442'}}}], 'application_context': {}, 'links': []}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.Order.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.Order.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class CardTest(unittest.TestCase):
    """Test class for Card"""

    def setUp(self):
        self.sample_dict = {'name': 'FB8BFDA518E218E8099BE4D5F9D69866144F77DF6DBCEE604F095DFD0C52ECC7', 'id': 'C03082E110AD992221D2D48627CA0DC23B50DC7275F4AB096FD2715B1B79DC7A', 'number': 'D527390A905CA2821070E0B5CC51E003D3BEDBE3FF84B800F5400E9888FD4CC5', 'expiry': '970C02B445DD62C945437800E44161069833736649FB79BF02BB75B1331A8837', 'security_code': '9FF8EABFCDF978DA9A3EE52796D5CF33B6DBD95B1FBEE128480F4EC7413B5624', 'last_digits': '29F27D073E756B324248BFDD794060152E6573CEEFFF61AD0C9EDD7491E5F690', 'card_type': 'B85C3C8DDCA93836F06FEBADE50FA62A451967F2F8CE70C5BAAD2D416AD1A050', 'billing_address': {'postal_code': 'A7C3D619A7581B2368625073C6BE144FAC7390C522074B261F4DEEAD3BAF0AC6', 'country_code': '510CB94EA524A96446CC99072AD46FA4B7ACD80D0D5DF2D2D3669680E582DB1A'}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.Card.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.Card.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class TokenTest(unittest.TestCase):
    """Test class for Token"""

    def setUp(self):
        self.sample_dict = {'id': '98A401EBCC748CA6E8FA8008D62901C6FCB32638E8D7865AE674E439849A2AF2', 'type': 'D366034A2DACE048CC6DEA7B5F5912A38FA2DF017FEFABF7CDF4A8F7F6963101'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.Token.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.Token.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class PaymentSourceTest(unittest.TestCase):
    """Test class for PaymentSource"""

    def setUp(self):
        self.sample_dict = {'card': {'name': '16FB6DABE3370331B8CFAB767976A2CDE81357A01B880B98D6728AC83C8492AF', 'id': '3F35E90928712EB4B917FAC970322456DF60EE65AB2852AD67E5A7BC275927E2', 'number': '5F0F8C61DDA28C3115FC404FA1DBF953A749DE9C08F1AFE7DD98B0892F6CD3D2', 'expiry': '24283BFDFB3D8D9668B145E92981942BDB16EAA1B190C156EEA4B00CC2CBE6F8', 'security_code': 'E1720DE7DFD577F2554C174DAD91F43A950F3B4B821524B7212E062560B5EDC2', 'last_digits': 'B79935EB44C0A312623A61977C518698B8B0C963EF30E109C0A3F6E7036D168B', 'card_type': 'BD57955D4C3CE82C2F9371EFADC5EBB30D3E940493A5685AAA5B1746CF01C643', 'billing_address': {'postal_code': '3EC9E16629C345E4BCCDAEF3F8DCDCA5BE22CDB67ADF3EC707C894C8BCD03BCA', 'country_code': '85FFCD1BBB3AD6F7555F8D24300AE69A51FD8F5FC9D671D2BB31F17CAF3836E1'}}, 'token': {'id': '64D0E18F1CE583E4EEC045DF46F2048EBC926DB5EA9DF271A61BF726372090BA', 'type': '13B722F7B05939B884E2C590B726E859056E54DA42F8C6B49E254EF3F2C03DD1'}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = orders.PaymentSource.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = orders.PaymentSource.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


if __name__ == '__main__':
    unittest.main()
