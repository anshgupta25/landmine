import hashlib
import json
from datetime import datetime as dt
from urllib.parse import urlparse
import requests
from random import randint

class BlockChain(object): #Blockchain with DPOS consensus algorithm

    def __init__(self):
        self.chain = []
        self.add_block(previous_hash = 0)
        self.unverified_txn = []  

        #List to store verified transactions
        self.verified_txn = []

        #Set containing the nodes in the network. Used set here to prevent the same node getting added again.
        self.nodes = set()

        #List containing all the nodes along with their stake in the network
        self.all_nodes = []

        #List of all the voting nodes in the network
        self.voteNodespool = []

        #List which stores all the nodes in descending order of votes received
        self.starNodespool = []

        #List to store the top 3 nodes with the highest (stake * votes_received)
        self.superNodespool = []

        #List to store the address of the delegate nodes selected for mining process
        self.delegates = []


        pass

    def add_block(self, previous_hash):
        now = dt.now()
        block_info = {'index': len(self.chain) + 1,
                 'timestamp': now.strftime("%d/%m/%Y %H:%M:%S"),
                 'transactions': self.unverified_txn,
                 'previous_hash': previous_hash
                 }
        #self.chain.append(block_info)
        return block_info

    def calc_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def new_txn(self, buyer_ID,seller_ID, property_ID, amt):
        now = dt.now()
        self.unverified_txn.append({
            'Buyer ID': buyer_ID,
            'Seller ID': seller_ID,
            'Property ID': property_ID,
            'Amount': amt,
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')
        })
        return self.last_block['index'] + 1

    def last_block(self):
        return self.chain[-1]
