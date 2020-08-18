import unittest
target = __import__("decode_test")

readConf = target.readConf
getConfFiles = target.getConfFiles
formatConfFiles = target.formatConfFiles
parseConfFile = target.parseConfFile
getHeaderInfo = target.getHeaderInfo
setHeaderInfo = target.setHeaderInfo
isWithinHeaderPulseRange = target.isWithinHeaderPulseRange
isWithinHeaderSpaceRange = target.isWithinHeaderSpaceRange
isWithinOnePulseRange = target.isWithinOnePulseRange
isWithinOneSpaceRange = target.isWithinOneSpaceRange
isWithinZeroPulseRange = target.isWithinZeroPulseRange
isWithinZeroSpaceRange = target.isWithinZeroSpaceRange
decode = target.decode

class TestDecode(unittest.TestCase):
    def test_readConf(self):
        # {'lircd.conf': }
        testconfig = [['begin', 'remote'], ['name', 'lircd.conf'], ['bits', '16'], ['flags', 'SPACE_ENC|CONST_LENGTH'], ['eps', '30'], ['aeps', '100'], ['header', '9139', '4495'], ['one', '622', '1631'], ['zero', '622', '517'], ['ptrail', '622'], ['repeat', '9141', '2213'], ['pre_data_bits', '16'], ['pre_data', '0x33B8'], ['gap', '108580'], ['toggle_bit_mask', '0x0'], ['begin', 'codes'], ['KEY_POWER', '33B8807F'], ['KEY_1', '33B88877'], ['KEY_2', '33B848B7'], ['KEY_3', '33B8C837'], ['KEY_4', '33B828D7'], ['KEY_5', '33B8A857'], ['KEY_6', '33B86897'], ['KEY_7', '33B8E817'], ['KEY_8', '33B818E7'], ['KEY_9', '33B89867'], ['KEY_0', '33B808F7'], ['KEY_A3', '33B8649B'], ['KEY_A2', '33B8A45B'], ['KEY_A1', '33B824DB'], ['KEY_MUTE', '33B844BB'], ['KEY_FULL', '33B8E41B'], ['KEY_A++', '33B8D42B'], ['KEY_+', '33B8946B'], ['KEY_-', '33B854AB'], ['KEY_ALARM', '33B804FB'], ['KEY_PLAY', '33B8847B'], ['KEY_FLASH', '33B8C43B'], ['KEY_DOWN', '33B850AF'], ['KEY_UP', '33B8C03F'], ['KEY_DISP', '33B8906F'], ['KEY_C-SET', '33B840BF'], ['KEY_T-SET', '33B8E01F'], ['KEY_MODE', '33B820DF'], ['KEY_CD-SET', '33B810EF'], ['KEY_ST', '33B8609F'], ['KEY_AL-SET', '33B8A05F'], ['KEY_RETURN', '33B800FF'], ['KEY_DIM', '33B858A7'], ['KEY_A4', '33B814EB'], ['KEY_C-F', '33B8D827'], ['end', 'codes'], ['end', 'remote']]
        testconfig2 = [['begin', 'remote'], ['name', 'Aiwa_DVD_Philips_Code_0140'], ['bits', '10'], ['flags', 'SPACE_ENC'], ['eps', '30'], ['aeps', '100'], ['header', '1623', '615'], ['one', '1629', '622'], ['zero', '500', '622'], ['repeat', '8967', '4467'], ['gap',
        '93949'], ['repeat_gap', '93945'], ['toggle_bit_mask', '0x0'], ['begin', 'codes'], ['KEY_POWER', '201'], ['KEY_SUBTITLE', '32C'], ['KEY_RED', '2F1'], ['KEY_GREEN', '390'], ['KEY_YELLOW', '370'], ['KEY_BLUE', '3AC'], ['KEY_EPG', '360'], ['KEY_INFO', '211'], ['KEY_OK', '28D'], ['KEY_BACK', '348'], ['KEY_MENU', '30C'], ['KEY_UP', '24D'], ['KEY_DOWN', '34C'], ['KEY_LEFT', '3CC'], ['KEY_RIGHT', '2CD'], ['KEY_REWIND', '2D9'], ['KEY_PLAYPAUSE', '350'], ['KEY_FORWARD', '358'], ['KEY_STOP', '2B1'], ['KEY_RECORD', '3EC'], ['KEY_CHANNELUP', '231'], ['KEY_CHANNELDOWN', '330'], ['KEY_1', '300'], ['KEY_2', '281'], ['KEY_3', '380'], ['KEY_4', '241'], ['KEY_5', '340'], ['KEY_6',
        '2C1'], ['KEY_7', '3C0'], ['KEY_8', '221'], ['KEY_9', '320'], ['KEY_0', '2A1'], ['KEY_MEDIA', '348'], ['end', 'codes'], ['end', 'remote']]
        result = readConf()
        self.assertEqual(result['lircd.conf'], testconfig)
        self.assertEqual(result['Aiwa_DVD_Philips_Code_0140'], testconfig2)
    
    def test_getConfFiles(self):
        arr = ["lircd.conf", "test.conf"]
        result = getConfFiles()
        self.assertEqual(result, arr)
        
        
    def test_formatConfFiles(self):
        arr = ['space 16777215', 'pulse 9093', 'space 4532', 'pulse 582']
        out = [['space', '16777215'],['pulse', '9093'],['space', '4532'], ['pulse', '582']]
        result = formatConfFiles(arr)
        self.assertEqual(result, out)
    
    def test_getHeaderInfo(self):
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        test = {'lircd.conf': [['begin', 'remote'], ['name', 'lircd.conf'], ['bits', '16'], ['flags', 'SPACE_ENC|CONST_LENGTH'], ['eps', '30'], ['aeps', '100'], ['header', '9139', '4495'], ['one', '622', '1631'], ['zero', '622', '517'], ['ptrail', '622'], ['repeat', '9141', '2213'], ['pre_data_bits', '16'], ['pre_data', '0x33B8'], ['gap', '108580'], ['toggle_bit_mask', '0x0']]}
        result = getHeaderInfo('lircd.conf', test)
        self.assertEqual(result, headerInfo)

    def test_setHeaderInfo(self):
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        result = setHeaderInfo(headerInfo)
        self.assertEqual(result, 1)
    
    def test_bad_setHeaderInfo(self):
        headerInfo = {}
        result = setHeaderInfo(headerInfo)
        self.assertEqual(result, -1)

    def test_parseConfFile(self):
        contents = []
        allDevices = {}
        testconfig = {'lircd.conf': [['begin', 'remote'], ['name', 'lircd.conf'], ['bits', '16'], ['flags', 'SPACE_ENC|CONST_LENGTH'], ['eps', '30'], ['aeps', '100'], ['header', '9139', '4495'], ['one', '622', '1631'], ['zero', '622', '517'], ['ptrail', '622'], ['repeat', '9141', '2213'], ['pre_data_bits', '16'], ['pre_data', '0x33B8'], ['gap', '108580'], ['toggle_bit_mask', '0x0'], ['begin', 'codes'], ['KEY_POWER', '33B8807F'], ['KEY_1', '33B88877'], ['KEY_2', '33B848B7'], ['KEY_3', '33B8C837'], ['KEY_4', '33B828D7'], ['KEY_5', '33B8A857'], ['KEY_6', '33B86897'], ['KEY_7', '33B8E817'], ['KEY_8', '33B818E7'], ['KEY_9', '33B89867'], ['KEY_0', '33B808F7'], ['KEY_A3', '33B8649B'], ['KEY_A2', '33B8A45B'], ['KEY_A1', '33B824DB'], ['KEY_MUTE', '33B844BB'], ['KEY_FULL', '33B8E41B'], ['KEY_A++', '33B8D42B'], ['KEY_+', '33B8946B'], ['KEY_-', '33B854AB'], ['KEY_ALARM', '33B804FB'], ['KEY_PLAY', '33B8847B'], ['KEY_FLASH', '33B8C43B'], ['KEY_DOWN', '33B850AF'], ['KEY_UP', '33B8C03F'], ['KEY_DISP', '33B8906F'], ['KEY_C-SET', '33B840BF'], ['KEY_T-SET', '33B8E01F'], ['KEY_MODE', '33B820DF'], ['KEY_CD-SET', '33B810EF'], ['KEY_ST', '33B8609F'], ['KEY_AL-SET', '33B8A05F'], ['KEY_RETURN', '33B800FF'], ['KEY_DIM', '33B858A7'], ['KEY_A4', '33B814EB'], ['KEY_C-F', '33B8D827'], ['end', 'codes'], ['end', 'remote']]}

        with open("C:/Users/RobSimon/Desktop/unittest project/lircd.conf", "r") as file:
            contents = formatConfFiles(file)
        file.close()

        allDevices = parseConfFile(allDevices, contents)
        self.assertEqual(allDevices, testconfig)


    def test_bad_parseConfFile(self):
        contents = []
        allDevices = {}
        testconfig = {}
        allDevices = parseConfFile(allDevices, testconfig)
        self.assertEqual(allDevices, testconfig)

    def test_isWithinHeaderPulseRange(self):
        #setting variables
        target.PERCENT = 0.35
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        setHeaderInfo(headerInfo)


        var = '9093'
        var2 = '5939'
        var3 = '-99999'
        var4 = '99999'
        var5 = '12338'
        var6 = '5941'
        var7 = '12337'
        result = isWithinHeaderPulseRange(var)
        result2 = isWithinHeaderPulseRange(var2)
        result3 = isWithinHeaderPulseRange(var3)
        result4 = isWithinHeaderPulseRange(var4)
        result5 = isWithinHeaderPulseRange(var5)
        result6 = isWithinHeaderPulseRange(var6)
        result7 = isWithinHeaderPulseRange(var7)
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, False)
        self.assertEqual(result4, False)
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
        self.assertEqual(result7, True)

    def test_isWithinHeaderSpaceRange(self):
        #setting variables
        
        target.PERCENT = 0.35
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        setHeaderInfo(headerInfo)

        var = '4495'
        var2 = '2921'
        var3 = '-99999'
        var4 = '99999'
        var5 = '6069'
        var6 = '6068'
        var7 = '2922'
        result = isWithinHeaderSpaceRange(var)
        result2 = isWithinHeaderSpaceRange(var2)
        result3 = isWithinHeaderSpaceRange(var3)
        result4 = isWithinHeaderSpaceRange(var4)
        result5 = isWithinHeaderSpaceRange(var5)
        result6 = isWithinHeaderSpaceRange(var6)
        result7 = isWithinHeaderSpaceRange(var7)
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, False)
        self.assertEqual(result4, False)
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
        self.assertEqual(result7, True)         

    def test_isWithinOnePulseRange(self):
        target.PERCENT = 0.35
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        setHeaderInfo(headerInfo)


        var = '622'
        var2 = '404'
        var3 = '405'
        var4 = '-99999'
        var5 = '840'
        var6 = '839'
        var7 = '99999'
        result = isWithinOnePulseRange(var)
        result2 = isWithinOnePulseRange(var2)
        result3 = isWithinOnePulseRange(var3)
        result4 = isWithinOnePulseRange(var4)
        result5 = isWithinOnePulseRange(var5)
        result6 = isWithinOnePulseRange(var6)
        result7 = isWithinOnePulseRange(var7)
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, True)
        self.assertEqual(result4, False)
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
        self.assertEqual(result7, False)    


    def test_isWithinOneSpaceRange(self):
        target.PERCENT = 0.35
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        setHeaderInfo(headerInfo)


        var = '1631'
        var2 = '1060'
        var3 = '1061'
        var4 = '-99999'
        var5 = '2202'
        var6 = '2201'
        var7 = '99999'
        result = isWithinOneSpaceRange(var)
        result2 = isWithinOneSpaceRange(var2)
        result3 = isWithinOneSpaceRange(var3)
        result4 = isWithinOneSpaceRange(var4)
        result5 = isWithinOneSpaceRange(var5)
        result6 = isWithinOneSpaceRange(var6)
        result7 = isWithinOneSpaceRange(var7)
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, True)
        self.assertEqual(result4, False)
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
        self.assertEqual(result7, False)

    def test_isWithinZeroPulseRange(self):
        target.PERCENT = 0.35
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        setHeaderInfo(headerInfo)


        var = '622'
        var2 = '404'
        var3 = '405'
        var4 = '-99999'
        var5 = '840'
        var6 = '839'
        var7 = '99999'
        result = isWithinZeroPulseRange(var)
        result2 = isWithinZeroPulseRange(var2)
        result3 = isWithinZeroPulseRange(var3)
        result4 = isWithinZeroPulseRange(var4)
        result5 = isWithinZeroPulseRange(var5)
        result6 = isWithinZeroPulseRange(var6)
        result7 = isWithinZeroPulseRange(var7)
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, True)
        self.assertEqual(result4, False)
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
        self.assertEqual(result7, False)


    def test_isWithinZeroSpaceRange(self):
        target.PERCENT = 0.35
        headerInfo = {
            "bits":"16",
            "zero_pulse":"622",
            "zero_space":"517",
            "one_pulse":"622",
            "one_space":"1631",
            "pre_data":"33B8",
            "pre_data_bits":"16",
            "header_pulse":"9139",
            "header_space":"4495"
            }
        setHeaderInfo(headerInfo)


        var = '517'
        var2 = '336'
        var3 = '337'
        var4 = '-99999'
        var5 = '698'
        var6 = '697'
        var7 = '99999'
        result = isWithinZeroSpaceRange(var)
        result2 = isWithinZeroSpaceRange(var2)
        result3 = isWithinZeroSpaceRange(var3)
        result4 = isWithinZeroSpaceRange(var4)
        result5 = isWithinZeroSpaceRange(var5)
        result6 = isWithinZeroSpaceRange(var6)
        result7 = isWithinZeroSpaceRange(var7)
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, True)
        self.assertEqual(result4, False)
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
        self.assertEqual(result7, False)

    def test_decode(self):
        arr = ['space 16777215', 'pulse 9093', 'space 4532', 'pulse 582', 'space 561', 'pulse 578', 'space 561', 'pulse 575', 'space 1676', 'pulse 579', 'space 1673', 'pulse 577', 'space 563', 'pulse 578', 'space 560', 'pulse 579', 'space 1676', 'pulse 577', 'space 1671', 'pulse 580', 'space 1672', 'pulse 578', 'space 562', 'pulse 576', 'space 1675', 'pulse 578', 'space 1675', 'pulse 579', 'space 1673', 'pulse 577', 'space 560', 'pulse 578', 'space 562', 'pulse 578', 'space 563', 'pulse 575', 'space 563', 'pulse 576', 'space 562', 'pulse 576', 'space 1674', 'pulse 578', 'space 562', 'pulse 602', 'space 536', 'pulse 608', 'space 529', 'pulse 578', 'space 561', 'pulse 577', 'space 561', 'pulse 578', 'space 1673', 'pulse 579', 'space 1676', 'pulse 603', 'space 535', 'pulse 576', 'space 1675', 'pulse 577', 'space 1674', 'pulse 579', 'space 1673', 'pulse 580', 'space 1672', 'pulse 581', 'space 1671', 'pulse 579', 'pulse 125379']
        deviceName = "lircd.conf"
        testconfig = {'lircd.conf': [['begin', 'remote'], ['name', 'lircd.conf'], ['bits', '16'], ['flags', 'SPACE_ENC|CONST_LENGTH'], ['eps', '30'], ['aeps', '100'], ['header', '9139', '4495'], ['one', '622', '1631'], ['zero', '622', '517'], ['ptrail', '622'], ['repeat', '9141', '2213'], ['pre_data_bits', '16'], ['pre_data', '0x33B8'], ['gap', '108580'], ['toggle_bit_mask', '0x0'], ['begin', 'codes'], ['KEY_POWER', '33B8807F'], ['KEY_1', '33B88877'], ['KEY_2', '33B848B7'], ['KEY_3', '33B8C837'], ['KEY_4', '33B828D7'], ['KEY_5', '33B8A857'], ['KEY_6', '33B86897'], ['KEY_7', '33B8E817'], ['KEY_8', '33B818E7'], ['KEY_9', '33B89867'], ['KEY_0', '33B808F7'], ['KEY_A3', '33B8649B'], ['KEY_A2', '33B8A45B'], ['KEY_A1', '33B824DB'], ['KEY_MUTE', '33B844BB'], ['KEY_FULL', '33B8E41B'], ['KEY_A++', '33B8D42B'], ['KEY_+', '33B8946B'], ['KEY_-', '33B854AB'], ['KEY_ALARM', '33B804FB'], ['KEY_PLAY', '33B8847B'], ['KEY_FLASH', '33B8C43B'], ['KEY_DOWN', '33B850AF'], ['KEY_UP', '33B8C03F'], ['KEY_DISP', '33B8906F'], ['KEY_C-SET', '33B840BF'], ['KEY_T-SET', '33B8E01F'], ['KEY_MODE', '33B820DF'], ['KEY_CD-SET', '33B810EF'], ['KEY_ST', '33B8609F'], ['KEY_AL-SET', '33B8A05F'], ['KEY_RETURN', '33B800FF'], ['KEY_DIM', '33B858A7'], ['KEY_A4', '33B814EB'], ['KEY_C-F', '33B8D827'], ['end', 'codes'], ['end', 'remote']]}
        arr = [x.split(" ") for x in arr]
        self.assertEqual(target.decode(arr, deviceName, testconfig), 'KEY_MODE')
    # def test_bad_type(self):
    #     data = 'test'
    #     with self.assertRaises(TypeError):
    #         result = sum(data)
    #arr = ['space 16777215', 'pulse 9093', 'space 4532', 'pulse 582', 'space 561', 'pulse 578', 'space 561', 'pulse 575', 'space 1676', 'pulse 579', 'space 1673', 'pulse 577', 'space 563', 'pulse 578', 'space 560', 'pulse 579', 'space 1676', 'pulse 577', 'space 1671', 'pulse 580', 'space 1672', 'pulse 578', 'space 562', 'pulse 576', 'space 1675', 'pulse 578', 'space 1675', 'pulse 579', 'space 1673', 'pulse 577', 'space 560', 'pulse 578', 'space 562', 'pulse 578', 'space 563', 'pulse 575', 'space 563', 'pulse 576', 'space 562', 'pulse 576', 'space 1674', 'pulse 578', 'space 562', 'pulse 602', 'space 536', 'pulse 608', 'space 529', 'pulse 578', 'space 561', 'pulse 577', 'space 561', 'pulse 578', 'space 1673', 'pulse 579', 'space 1676', 'pulse 603', 'space 535', 'pulse 576', 'space 1675', 'pulse 577', 'space 1674', 'pulse 579', 'space 1673', 'pulse 580', 'space 1672', 'pulse 581', 'space 1671', 'pulse 579', 'pulse 125379']

if __name__ == '__main__':
    unittest.main()