## Solution

1. Find End of Central Directory of zip file
2. Notice that there is are some extra bytes added to end of EOCD, with padding before and after
3. base64 decode the extra bytes to get flag

### Unintended Solve

1. strings the zip file
2. base64 decode the last line from strings to get flag
