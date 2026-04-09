# Poki

Poki is an extremely minimal pastebin-like server where users can upload files to the server from a command line.

To start the server, run it with
```bash
POKI_API_KEY="<your api key here>" uvicorn main:app
```

You can generate the API key with `openssl rand -base64 32`. Or it can be anything you want /shrug

## Uploading Files

You can make an upload to the server using cURL like
```bash
cat file.txt | curl --data-binary @- https://poki.example.com/ -H "Authorization: Bearer <your api key here>"
```

It will return the URI of the file.

I recommend making an alias for that curl command.

## Deleting Files

```bash
curl -X DELETE https://poki.example.com/lipu/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -H "Authorization: Bearer <your api key here>"
```