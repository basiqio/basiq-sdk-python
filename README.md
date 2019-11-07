## Deprecated

This project is deprecated and is no longer maintained. Please use [Go](https://github.com/basiqio/basiq-sdk-golang) or [NodeJS](https://github.com/basiqio/basiq-sdk-nodejs) SDK instead.

# Basiq.io Python SDK

This is the documentation for the Python SDK for Basiq.io API.

This SDK is compatible with Python 3

## Introduction

Basiq.io Python SDK is a set of tools you can use to easily communicate with Basiq API.
If you want to get familiar with the API docs, [click here](https://basiq.io/api/).

The SDK is organized to mirror the HTTP API's functionality and hierarchy.
The top level object needed for SDKs functionality is the Session
object which requires your API key to be instantiated.
You can grab your API key on the [dashboard](http://dashboard.basiq.io).

## Changelog

0.9.0beta - Initial release

## Getting started

Now that you have your API key, you can use the following command to install the SDK:

```bash
pip install basiq
```

Import the package 

```python
import basiq
```

And input the endpoint you wish to target
```python
api = basiq.API("https://au-api.basiq.io")
```

## Common usage examples

### Fetching a list of institutions

You can fetch a list of supported financial institutions. The function returns a list of Institution structs.

```python
import basiq

api = basiq.API("https://au-api.basiq.io")
session = basiq.Session(api, "YOUR_API_KEY")

institutions = session.getInstitutions()
```

You can specify the version of API when instantiating Session object. When the version is not specified, default version is 1.0.

```python
import basiq

api = basiq.API("https://au-api.basiq.io")
session = basiq.Session(api, "YOUR_API_KEY", "2.0")

institutions = session.getInstitutions()
```

### Creating a new connection

When a new connection request is made, the server will create a job that will link user's financial institution with your app.

```python
import basiq

api = basiq.API("https://au-api.basiq.io")
session = basiq.Session(api, "YOUR_API_KEY")

user = session.forUser(userId)

job = user.createConnection({
    "loginId": "gavinBelson",
    "password": "hooli2016",
    "institution": {
        "id": "AU00000"
    }
})

// Poll our server to wait for the credentials step to be evaluated
connection = job.waitForCredentials(1000, 60)
```

### Fetching and iterating through transactions

In this example, the function returns a transactions list struct which is filtered by the connection.id property. You can iterate
through transactions list by calling Next().

```python
import basiq

api = basiq.API("https://au-api.basiq.io")
session = basiq.session(api, "YOUR_API_KEY")

user = session.forUser(userId)

fb = basiq.utils.FilterBuilder()
fb.eq("connection.id", "conn-id-213-id")
transactions = user.getTransactions(fb)

while transactions.next():
    print("Next transactions len:", len(transactions.data))

```

## API

The API of the SDK is manipulated using Services and Entities. Different
services return different entities, but the mapping is not one to one.

### Errors

If an action encounters an error, you will receive an HTTPResponseException
instance. The class contains all available data which you can use to act
accordingly.

##### HTTPError class fields
```python
correlationId #string
data #map
```

You can invoke the ```get_message()``` method or just str(error) to get the messages. Messages will
be concatenated with a comma.

Check the [docs](https://basiq.io/api/) for more information about relevant
fields in the error object.

### Filtering

Some of the methods support adding filters to them. The filters are created
using the FilterBuilder class. After instantiating the class, you can invoke
methods in the form of comparison(field, value).

Example:
```python
import basiq

fb = basiq.utils.FilterBuilder()
fb.eq("connection.id", "conn-id-213-id").gt("transaction.postDate", "2018-01-01")
transactions = user.getTransactions(fb)
```

This example filter for transactions will match all transactions for the connection
with the id of "conn-id-213-id" and that are newer than "2018-01-01". All you have
to do is pass the filter instance when you want to use it.
