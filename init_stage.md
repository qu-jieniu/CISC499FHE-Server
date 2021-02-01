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
  - `calc(a, b, operation)`
    - `addition(obj, dataType)`
    - `subtraction(obj, dataType)`
    - `multiply(obj, dataType)`
  - `dataCommunication(addr)`
    - `listen()`
    - `send()`
    - `receive()`
  - `dataStore()`
    - `toDatabase()`

### `p` Explanation
The padding is used to address the previous issue with `x < m`.\
The modification is done based on the profs algorithm.

Encryption: `x' = (a +/* p) % m`, `q = (a +/m p) // m`.\
Decryption:
```
a+b = (a'+b') + (q1+q2)*m - 2*p
a*b = [ (a'+b') + (a'*q2 + b'*q1 + q1*q2*m)*m ] // k^2
```
