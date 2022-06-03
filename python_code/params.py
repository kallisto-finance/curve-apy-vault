
balance_threshold = 1e8  # lower bound for the balance
balance_ratio_threshold = 0.8  # higher bound for the balance ratio

name_to_address = {'3pool':'0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7',
             'aave':'0xDeBF20617708857ebe4F679508E7b7863a8A8EeE',
             'ankreth':'0xA96A65c051bF88B4095Ee1f2451C2A9d43F53Ae2',
             'iearn':'0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B',
             'compound':'0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56',
             'eurs':'0x0Ce6a5fF5217e38315f87032CF90686C96627CAA',
              'ren':'0x93054188d876f558f4a66B2EF1d97d16eDf0895B',
             'steth':'0xDC24316b9AE028F1497c275EB9192a3Ea0f67022',
             'frax':'0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B',
             'mim':'0x5a6A4D54456819380173272A5E8E9B9904BdF41B',
             'tricrypto2':'0xD51a44d3FaE010294C616388b506AcdA1bfAAE46',
              'alusd':'0x43b4FdFD4Ff969587185cDB6f0BD875c5Fc83f8c',
              'susdv2':'0xA5407eAE9Ba41422680e2e00537571bcC53efBfD'}

"""
cvxcrv, aleth, fpi2pool: addresses can't be found on
https://curve.fi/contracts
"""

address_to_name = {v: k for k, v in name_to_address.items()}