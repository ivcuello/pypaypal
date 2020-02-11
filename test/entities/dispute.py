
"""test module for pypaypal.entities.dispute
"""

import unittest

from pypaypal.entities import dispute


class BuyerTest(unittest.TestCase):
    """Test class for Buyer"""

    def setUp(self):
        self.sample_dict = {'name': '4C26F0A19BAA196764E547C1A450F05833F4FE25F958CD9D3056B2D514BCAA56'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.Buyer.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.Buyer.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class ItemInfoTest(unittest.TestCase):
    """Test class for ItemInfo"""

    def setUp(self):
        self.sample_dict = {'notes': '422446BA691D4A8FED23BF96BEC71AC7F5AEFE559C968A0AA6D2787610BDB591', 'reason': '3829D6119FDB3085610634C7852ED518407AC12F6672E7D0BD734FD604A74940', 'item_id': '3173F7283D29EDAE5531CC5D2F6F0B7A90BE3E6BCDCF7F87B072642419413BDA', 'dispute_amount': {'value': '048F07FB668C99E69266F18EA6BC7787BBDAE799D5A640E2FF84BC2E84EF8882', 'currency_code': 'USD'}, 'item_description': 'DE1E89CC7F8E5E7860834CCB257F4C32AA1497EBDE3E05609E6D05D0014E2152', 'partner_transaction_id': '2EF0D520905921DB34F5B9E154EF0C5AFDFB494645395DE9740CEA004A0BD745'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.ItemInfo.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.ItemInfo.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DisputeTransactionTest(unittest.TestCase):
    """Test class for DisputeTransaction"""

    def setUp(self):
        self.sample_dict = {'items': [{'notes': '018E67A5DF5DC12389B2EEF65B40658D3F259F8B3B0E4871DBCFB3944660D685', 'reason': '6ABCA1C3B7DD91FDCBAAB741A8F3456F4429D30187C440659C267FCF9E1D4DAD', 'item_id': 'A3D8C2EA30E62CD02B721118D2E3DD1A56ED08D0420F79F9BEEC65D6364FD441', 'dispute_amount': {'value': '4CE4A1C13E82D241061429321E85658BB321408CC2865C9CA40C2DE498C792E4', 'currency_code': 'USD'}, 'item_description': '843D0EAA8E5E1A469F062A091D64BFF71B6BB9386DBA32858B92837AC4E3620B', 'partner_transaction_id': '5850B755D9EC677CA500E0983FE6E705BD1AA286411D0373E84CBA96B3663F2D'}], 'buyer': {'name': '117D7B094CDD8C402A7D1AB7107E26113A967BF245793D781EAFE209C2D30065'}, 'seller': {'name': '2FBE7B2ED2B7F3D0904CD95D8927AA447F2796426F4AF314F078BF3931D10FF7', 'email': '953B5BF33146802CD3BAC47652C985B883DB2E3AB4700BE086230383CFD1DCCA', 'merchant_id': 'E476C22DE6B10242CD13691F4A6C9ED876C08F601975911839373567505AEF02'}, 'custom': '0902B36219DEB17EAB51D4E184CA0DB314148DA173ED720A7455580AADB45B29', 'messages': [{'content': '38FC90581D134038450346450A298625C8714E28AABD6E45D66CD56F842E34FB', 'posted_by': '4DE02337CF5CA127D5CFD30767E96642B6A2F0D143D3DE17C91B615C57EF6C51', 'time_posted': '581D6B249058DEDF1C6E4493514CCCD27003F0A34832F2A85DA378F678513D5F'}], 'gross_amount': {'value': '3268FB42AB46A4544A25AAD8C25BDED28FCEE9BAFD3C832EFC7D993C0B143D98', 'currency_code': 'USD'}, 'invoice_number': '19F2796487A235D8CE034E0DBF5DBDF7A24D6BA6317EA6C32004AFBBF836BD76', 'transaction_status': '2F22A78F3B5C06E1AACEB87513E5FA1BF31E7B2FF6E86E38FA7613373D4E80B8', 'buyer_transaction_id': '5782A2B7C84B041BBCA536A8C99A8F4768012D8289142F9849B2FE0B96BE343E', 'seller_transaction_id': '29AA4986A3BFF323EAE7E14A7CCB3FAEBA6F9F4CE1BA44261CD78235F9B633E4'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.DisputeTransaction.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.DisputeTransaction.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DisputeTrackerTest(unittest.TestCase):
    """Test class for DisputeTracker"""

    def setUp(self):
        self.sample_dict = {'carrier_name': '6840AB6F33D6E9D86C65A7BDD584AE3AD571A46BC5EAD32659E9A62856A4F5DA', 'tracking_number': '04F75B4A3BA21060B6AFF4FEF093776166890195CA56A0E9FD9A4BE1BE9C75F9'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.DisputeTracker.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.DisputeTracker.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class RefundIdTest(unittest.TestCase):
    """Test class for RefundId"""

    def setUp(self):
        self.sample_dict = {'refund_id': '7F8CC18138D84E98FF96E513470AB8287AB0E5170D63E28C1346400B8862054E'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.RefundId.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.RefundId.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DisputeEvidenceInfoTest(unittest.TestCase):
    """Test class for DisputeEvidenceInfo"""

    def setUp(self):
        self.sample_dict = {'tracking_info': [{'carrier_name': '6F368597D0C21AC429533FB0A3139AE968139D0D8D04DDEAEF096E3CCCD93731', 'tracking_number': '7AEED8E6D4491A72E571A5C890CAE207C148D9149C87C61226C9CF6FF13BD8D3'}], 'refunds_ids': [{'refund_id': 'B4B06194399555D6597CE0DBA91914E1B960B85ECEDEAD6AF83745AD9127225F'}]}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.DisputeEvidenceInfo.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.DisputeEvidenceInfo.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DocumentTest(unittest.TestCase):
    """Test class for Document"""

    def setUp(self):
        self.sample_dict = {'name': '1B14D80EF75280380EF284A70EBD87BDC47B9FE745B73B16FB71A75D813E985B'}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.Document.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.Document.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DisputeEvidenceTest(unittest.TestCase):
    """Test class for DisputeEvidence"""

    def setUp(self):
        self.sample_dict = {'notes': 'E455FD6F54A8361DBD077026698C16D36D03D5B92D91AF45BDFB1A1C8C9DBF68', 'item_id': '09A17A8490599EDDD5DCD1963AA0CBD6B8ECC71DB8C309F42FCA24051ACB7FC5', 'document': {'name': '55A6E95A43AF9E180C13DC20B686A3E4E4F7120E24BED481C2B902114374D949'}, 'evidence_type': '6CF728DE6017B69AFFA6E7DD905ACA3407B3935D071B21EC2CAF4C9709B84254', 'evidence_info': {'tracking_info': [{'carrier_name': 'B5EB3643A3E229A83D26A7D9CF44D4B098E3717026FB1249744449F6122EE24F', 'tracking_number': '6C238745F8F7D194D3D34381FA06ADA96F0487D25C9787680697C139F2B3D484'}], 'refunds_ids': [{'refund_id': '84EA4D0051156DA5D94BD986B9DC32568E8089445BCA968B45B7667E32940ADE'}]}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.DisputeEvidence.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.DisputeEvidence.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DisputeOutcomeTest(unittest.TestCase):
    """Test class for DisputeOutcome"""

    def setUp(self):
        self.sample_dict = {'outcome_code': 'FF4A795CD50A86D86DE8E8649C13A2730AE27C764D7035F08D3DF80C36D96812', 'amount_refunded': {'value': '3E0F95B8783DCA12CCCCD51C6983CC47E246ABA5702545A8B1FEA1DAE56903B9', 'currency_code': 'USD'}}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.DisputeOutcome.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.DisputeOutcome.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


class DisputeTest(unittest.TestCase):
    """Test class for Dispute"""

    def setUp(self):
        self.sample_dict = {'offer': {'value': '3B4308F1114D00B4C4209630AB891AF51ABDFA2A7BBF17CE5DB1395D1CECB2E2', 'currency_code': 'USD'}, 'reason': 'D3A1A71C2756328A9E22EF35C69E0D4F0A91AB23348BD4796A977F264010779B', 'status': 'C8E36CCCFA2ACC6DB079C4D12D0FEECC5A3297DD1FB50B0F8D4166E5326F1215', 'messages': [{'content': '4EB8E6D78B1EC6D65F1AC42A8A42D8C01C1BD36F4D061FB2BA916AEE4A262913', 'posted_by': '204F801A05E093713859400A3A0C2246D50D1DE598E3CF3D4B4AF5CC64E4DD72', 'time_posted': 'A4586535761CF0BB102FF46C527C2B0B9E9EC750C7DAF678EF7F6FB9F42928E3'}], 'dispute_id': '400593779CEA0B38BF0A23FA04DD89D320E79B070CD5E4B5F158295C021EF1C6', 'dispute_amount': {'value': 'AEC3187E4E283816550E42EEB9C30D8ED662AD11BA6EA4E5C2E547575A77E5E1', 'currency_code': 'USD'}, 'dispute_state': 'AF8CBE337EAA7AD9038C95D3710307851A56AD80FACA9E002552C7B7E279500B', 'dispute_channel': '90315E04DFC3D1D675F20DD228040BBB31C83C7879202FA98B7E7C1FB7A9F673', 'dispute_outcome': {'outcome_code': '72F3E4E49B093738E3679BE7CABAFE28A8E0D1805849EDFE74F4AAF6533E8BDF', 'amount_refunded': {'value': '3C82D88E6629F1B54D1245126F14149F633114B81DEDFC99638DFA6E9444CD31', 'currency_code': 'USD'}}, 'disputed_transactions': [{'items': [{'notes': '3A007609FB900874978E112C7107B97619E73BEFA1E848E33BB6D87C36718ECD', 'reason': 'D0762B066B3A0E7129F0425DBA389C88206B2D78725ACA7DA6D29E47C424457C', 'item_id': 'A931265A28A87146D966E5CA6C67575CAE8E9FEA308502A2FC2CEEE8B55B7D1A', 'dispute_amount': {'value': '9898E6C5417861D689F27809769588AD4E06B152AEA40646E6FE9CA39E7A707B', 'currency_code': 'USD'}, 'item_description': '56C22AF911B786A40B9459DDB6DC8ACC5067B385E7145698FA27619F3698D3D3', 'partner_transaction_id': '9852534DF72FEE75FC9618BC17BCAF04987C01DC0FE95A3AEC9D7A56B0F08CEA'}], 'buyer': {'name': '6333D8878D23C6F211273D38F4A448D47E8689D79A5881DE3D34F647C1150A57'}, 'seller': {'name': 'D20EBD07987EC7996E7D6C972607E68B41961C20A4B5C3938DD9F14EF3E98EB1', 'email': '62404EDB46C48984FF2A48EB152DF21FB65BC25C955518550FF81284B3D794B5', 'merchant_id': 'DA78F58FC57C18CD890C7645870EB558CB306A1E03C0141EEE6812E7FC1F16D3'}, 'custom': '3195FDD04EE3F98170D06A8CF1B2C22AA52D18A7C6A40DA0120DD51E31C17D02', 'messages': [{'content': '3498A0A6F64005E0124BD4FA40B8C0C9A3367774BFACA7E6A830EFFA50FB87CE', 'posted_by': '08A9F635474B5D227EF1D277BB2A49697DB313D48D07242483B2F73F2C99414E', 'time_posted': '9FD8A906C64FFAA9307A45380ABBFD41F5F942CC9AA0F0EF8A25CF26E4B709DB'}], 'gross_amount': {'value': '90202567CBF2000D90895B52F0D26089C8BC13426B5ABF0D3E04422108D2FA3F', 'currency_code': 'USD'}, 'invoice_number': '42D2B249D639BC541258951A0EE96CC8989C98CCE463FEA1D18A3BD2E14E1706', 'transaction_status': '8B97546C5EB475581810A214F671F2DB8255FA6CF01618BBC1F32C729C8E3C76', 'buyer_transaction_id': '6CB8B66B1B2634648CBEE2BA3EBC56B9FF522F972594DE9DCF5C2E55BD2ACDF1', 'seller_transaction_id': '67D643220E3A45192AC0291B6428C680506F608E6782B103867A0A9B68732D51'}], 'dispute_life_cycle_stage': '30C3C5C913E0D6370B09BBEA5D3DB4642E2DCD58816FAF4C9AFD02E0BFABB5F6', 'links': []}

    def test_serialize_from_json(self):
        """Testing json_response serialization factory method"""        
        e = dispute.Dispute.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        """Testing instance from dict factory method"""
        e = dispute.Dispute.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)


if __name__ == '__main__':
    unittest.main()
