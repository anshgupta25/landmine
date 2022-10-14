

from flask import Flask, jsonify, request

from bchain import Blockchain

app = Flask(__name__)
bchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    current_port = "localhost:"+ str(port)
    if(current_port in bchain.delegates):
        # response = {
        #         'message': "New block mined!",
        #         'index': "",
        #         'transactions': "",
        #         'previous_hash': ""
        #     }
        # return jsonify(response),200
        if len(bchain.unverified_txn) >= 2:
            last_block = bchain.last_block
            previous_hash = bchain.calc_hash(last_block)
            ver_txn = bchain.validate_txn()
            block = bchain.add_block(previous_hash)
            response = {
                'message': "New block mined!",
                'index': block['index'],
                'transactions': block['transactions'],
                'previous_hash': block['previous_hash']
            }
            print(len(bchain.unverified_txn))
            return jsonify(response), 200

        else:
            response = {
                'message' : 'Not enough transactions to mine a new block and add to chain!'
            }
            print(len(bchain.unverified_txn))
            return jsonify(response),400

    

    else:
        response = {
            'message': 'You are not authorised to mine block! Only delegates can mine.'
        }
        return jsonify(response),400


@app.route('/add/node', methods=['POST'])
def add_nodes():
    values = request.get_json()
    required = ['nodes','stake']
    
    if not all(value in values for value in required):
        return 'Error',400

    bchain.add_node(values['nodes'], values['stake'])
    
    response = {
        'message': 'New nodes have been added.',
        'total_nodes': list(bchain.nodes)
    }
    print(bchain.nodes)
    return jsonify(response), 201


@app.route('/add/txn', methods=['POST'])
def new_txn():
    values = request.get_json()
    required = ['sender_ID', 'buyer_ID', 'property_ID','amt']

    if not all(value in values for value in required):
        return 'Please enter sender_id, buyer_ID, property_ID and amt.', 400
    
    idx = bchain.new_txn(values['sender_ID'], values['buyer_ID'], values['property_ID'], values['amt'])

    response = {
        'message': f'Transaction will be added to block {idx}'
    }
    return jsonify(response), 201


@app.route('/show_full_chain', methods=['GET'])
def show_chain():
    response = {
        'chain': bchain.chain,
        'length': len(bchain.chain)
    }
    return jsonify(response), 200


@app.route('/voting',methods=['GET'])
def voting():
    bchain.vote_grp = []
    bchain.star_grp = []
    bchain.super_grp = []
    if(port == 5000):
        show_votes = bchain.voting_power()

        response ={
            'message': 'Voting Results: ',
            'nodes': bchain.vote_grp
            }
        
        return jsonify(response),200
        
    else:
        response={
            'message': 'You are not authorized to conduct the election process!'
        }
        return jsonify(response),400


@app.route('/show/delegates',methods=['GET'])
def delegates():
    bchain.delegates = []
    show_delegates = bchain.delegates_selection()

    response={
        'message': 'The 3 delegate nodes selected for block mining are: ',
        'node_delegates': bchain.delegates
    }
    return jsonify(response),200


@app.route('/sync/delegates',methods=['GET'])
def syncro_delegates():
    syncro_delegates = bchain.synchro()

    response ={
        'message': 'The delegate nodes are: ',
        'node_delegates': bchain.delegates
    }
    return jsonify(response),200





if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Listening on port')
    args = parser.parse_args()
    port = args.port
    app.run(host = '0.0.0.0', port = port)