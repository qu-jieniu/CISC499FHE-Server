# Initial staging

### Used packages
- `pyca/cryptography` regularly maintained, symmetric-key focused.

### Functions
- FHE_Client   
  - `keyGen()`
    - Using package function to generate 128-bit key
  - `encrypt(obj, dataType=int)`
    - `convertFromPlain()`
  - `decrypt(obj, dataType=int)`
    - `convertToPlain()`
  - `dataCommunication(addr)`
    - `listen()`
    - `send()`
    - `receive()`

- FHE_Server  
  - `eval(a, b, operation)`
    - `addition(obj, dataType)`
    - `subtraction(obj, dataType)`
    - `multiply(obj, dataType)`
  - `dataCommunication(addr)`
    - `listen()`
    - `send()`
    - `receive()`
  - `dataStore()`
    - `toDatabase()`
