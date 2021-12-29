from bitcoinrpc.authproxy import AuthServiceProxy
from script4Task.credentials import rpc_username, rpc_password, rpc_hostname, rpc_port

rpc_connection = AuthServiceProxy(f'http://{rpc_username}:{rpc_password}@{rpc_hostname}:{rpc_port}')

print(rpc_connection.getblockcount())