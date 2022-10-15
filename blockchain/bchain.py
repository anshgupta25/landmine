from audioop import add
import errno
import hashlib
import json
from typing import List
from datetime import datetime as dt
from urllib.parse import urlparse
import requests
from random import randint

# from blockchain.main import delegates

class Blockchain(object): 
    def __init__(self):
        self.chain = [] #list for storing the full blockchain after mining
        
        self.unverified_txn = []  #list for storing the transactions which need to be added to the block

        self.verified_txn = [] #list of all the transaction verified till now

        self.nodes = set() # set of nodes i.e the miners / computers for mining/verificiation of blocks

        self.all_nodes = [] #list of all nodes

        self.vote_grp = [] #the voting group consisting of all the nodes

        self.star_grp = [] #the group sorted in decreasing order of voting power

        self.super_grp = []# final group selected for delegates

        self.delegates = [] #the delegates nodes of the blockchain
        
        self.txn_hashes = [] #hash values of all the transactions
        
        self.unverified_hash =[] #list of unverified hashes

        self.txns = [] #list of all the transactions
        
        self.add_block(previous_hash = 0)

    def add_block(self, previous_hash):
        txn_hash_adding = self.test()
        now = dt.now()
        block_info = {'index': len(self.chain) + 1,
                 'timestamp': now.strftime("%d/%m/%Y %H:%M:%S"),
                 'transactions': self.unverified_txn,
                 'previous_hash': previous_hash,
                 'merkle_root': txn_hash_adding
                 }
        self.chain.append(block_info)
        self.unverified_txn = []
        self.unverified_hash =[]
        return block_info
    
    def test(self):
        elems = self.unverified_hash
        mtree = MerkleTree(elems)
        print (elems)
        return mtree.getRootHash()
        
    def validate_txn(self):
        for i in range(len(self.unverified_txn)):
            self.verified_txn.append(self.unverified_txn[i])

    

    def new_txn(self, buyer_ID,seller_ID, property_ID, amt):
        now = dt.now()
        txn_info={
            'Buyer ID': buyer_ID,
            'Seller ID': seller_ID,
            'Property ID': property_ID,
            'Amount': amt,
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.unverified_txn.append(txn_info)
        txn_hash_curr = self.calc_hash_txns(txn_info)
        self.unverified_hash.append(txn_hash_curr)
        
        # return self.last_block['index'] + 1

    
    def calc_hash(self, block_info):
        block_string = json.dumps(block_info.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def calc_hash_txns(self, txn_info):
        block_string = json.dumps(txn_info, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def txn_history(self, prop_ID):
        for i in range(len(self.verified_txn)):
            if self.verified_txn[i]['Property ID'] == prop_ID:
                self.txns.append(self.verified_txn[i])
        return self.txns

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
        self.all_nodes = list(self.nodes)
        for x in self.all_nodes:
            votepow= list(x)
            votepow.append(x[1]*randint(0,10))
            self.vote_grp.append(votepow)
            
        # print(self.vote_grp)
        
    def delegates_selection(self):
        self.delegates=[]
        self.star_grp = sorted(self.vote_grp, key = lambda vote: vote[2],reverse = True)
        # print(self.star_grp)

        for x in range(3):
            self.super_grp.append(self.star_grp[x])
        # print(self.super_grp)

        for y in self.super_grp:
            if(y[0] not in self.delegates):
                self.delegates.append(y[0])
            
        print(self.delegates)
    
    
    def synchro(self):
        r = requests.get('http://localhost:5000/show/delegates')
        print(r)

        if(r.status_code == 200):
            delegates = r.json()['node_delegates']
            self.delegates = delegates[0:3]
            print(self.delegates)


class Node:
    def __init__(self, left, right, value: str, content, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.value))

    def copy(self):
        """
        class copy function
        """
        return Node(self.left, self.right, self.value, self.content, True)


class MerkleTree:
    def __init__(self, values: List[str]) -> None:
        self.__buildTree(values)

    def __buildTree(self, values: List[str]) -> None:

        leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())  # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        if(len(nodes)==0):
            return
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())  # duplicate last elem if odd number of elements
        half: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)

        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        content: str = f'{left.content}+{right.content}'
        return Node(left, right, value, content)

    def printTree(self) -> None:
        self.__printTreeRec(self.root)

    def __printTreeRec(self, node: Node) -> None:
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")
                
            if node.is_copied:
                print('(Padding)')
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)

    def getRootHash(self) -> str:
        if(self.root == None):
            return "0"
        print(self.root)
        return self.root.value
