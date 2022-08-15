# godaddy-ddns
* Python script for turning your dynamic ip static.
* Updates your DNS record to your local ip if they dont match (runs every 10 minutes)
* Currently only supports the GoDaddy.com DNS server 
# Usage
* ## Docker (Reccomended)
  * ### docker cli:
  ```
  docker run -e DOMAIN=example.com -e HOST=your_host -e API_KEY=your_godaddy_api_key -e API_SECRET=your_godaddy_api_secret  nub31/godaddy_ddns
  ```
  * ### docker-compose:
  ```
  TODO
  ```
* ## python
  Change the env variables to your values.
  Then run:
  
  ```
  pip install -r requirements.txt
  ```
  ```
  python main.py
  ```
