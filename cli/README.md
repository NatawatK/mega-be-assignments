# CLI ERC20 Helper assignment

## Pre-requisite
- Python version >3.6 (3.9.x recommend)
- Pip (make sure you are using correct one if you have multiple versions of python)

## Step to run program
### install requirement packages 
```bash
pip install -r requirements.txt

pip3 install -r requirements.txt

python3 -m pip install -r requirements.txt
```
### prepare env file
   1. create new env file named `.env` inside `cli` directory (you can take at .env.example for reference)
   2. add following config
      1. HTTP_ENDPOINT => your http endpoint
      2. WS_ENDPOINT => your web socket endpoint
      3. USE_WEB_SOCKET => 0 if you want to use http and 1 if you want to use websocket
      4. ETHERSCAN_API_KEY => this is optional, you can leave it as blank

### run the scripts
```bash
# make sure your current directory is cli

# view all usage
python3 main.py --help


# command examples
# show contract detail
python3 main.py detail <contract_address>

# get balance of address in contract
python3 main.py balance-of <contract_address> <target_address>

# subscribe transaction of contract
python3 main.py watch-tx <contract_address>

# get latest N transaction of contract
python3 main.py latest-tx <N> <contract_address>

# get top N holders of contract
python3 main.py holders <N> <contract_address>
```

## Improvement proposal
1. get holders function (this is not working 100%)
   1. This function is pretty straight-forward it's get all Transfer event and try to solve balances of holder
   2. There is some limitations of Infura/Alchemy that it cannot return big response (limit as 10k records)
   3. I tried to use divide and contour but seems it doesn't help
   4. holders function should be the job execution queue can can be multiple-processor
   5. result should keep in cache or persistence storage
2. ABI
   1. currently, I hard-coded abi into the code
   2. better way it to read from file
   3. or even better is to query ABI from some verified sources. e.g. Ehterscan
3. Logging
   1. there are lots of print statement, I think we can use logging lib to help manage these log
4. Testing 
   1. it should have proper unit testing