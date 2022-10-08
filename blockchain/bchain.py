from audioop import add
import hashlib
import json
from datetime import datetime as dt
from urllib.parse import urlparse
import requests
from random import randint

class Blockchain(object): #Blockchain with DPOS consensus algorithm

    def __init__(self):
        self.chain = []
        
        self.unverified_txn = []  

        #List to store verified transactions
        self.verified_txn = []

        #Set containing the nodes in the network. Used set here to prevent the same node getting added again.
        self.nodes = set()

        #List containing all the nodes along with their stake in the network
        self.all_nodes = []

        #List of all the voting nodes in the network
        self.vote_grp = []

        #List which stores all the nodes in descending order of votes received
        self.star_grp = []

        #List to store the top 3 nodes with the highest (stake * votes_received)
        self.super_grp = []

        #List to store the address of the delegate nodes selected for mining process
        self.delegates = []
        
        self.add_block(previous_hash = 0)

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
    
    def is_chain_valid(self,chain):
        prev_block = chain[0]
        pos =1
        
        while pos<len(chain):
            block = chain[pos]
            if(block['prev_hash']!=self.calc_hash(prev_block)):
                return False
            
            prev_block = chain[++pos]
            
        return True
    
    
    def add_node(self, address, stake):
        parsed_url = urlparse(address)
        authority = stake
        self.nodes.add((parsed_url.netloc,authority))
        
        
    def voting_power(self):
        for x in self.nodes:
            votepow= list(x)
            votepow.append(x[0]*randint(0,10))
            self.vote_grp.append(votepow)
            
        # print(self.vote_grp)
        
    def delegates_selection(self):
        self.star_grp = sorted(self.vote_grp, key = lambda vote: vote[2],reverse = True)
        # print(self.star_grp)

        for x in range(3):
            self.super_grp.append(self.star_grp[x])
        # print(self.super_grp)

        for y in self.super_grp:
            self.delegates.append(y[0])
            
        print(self.delegates)
    
    
    def synchro(self):
        r = requests.get('http://localhost:5000/delegates/show')
        print(r)

        if(r.status_code == 200):
            delegates = r.json()['node_delegates']
            self.delegates = delegates[0:3]
            print(self.delegates)
