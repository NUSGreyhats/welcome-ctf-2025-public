## Solve

If you run `strings crazy_gifarfe.gif`, you will see some interesting strings near the end:

```text
META-INF/
META-INF/MANIFEST.MF
...
dFrLc/
dFrLc/f0vtW.wfmHf
...
META-INF/PK
META-INF/MANIFEST.MFPK
dFrLc/PK
dFrLc/f0vtW.classPK
```

Googling this, you can figure out that it might be a JAR file.

Then just run `java -jar crazy_gifarfe.gif` to print the flag

## Explanation

Polyglots, in a security context, are files that are a valid form of multiple different file types. For example, a GIFAR is both a GIF and a JAR file. There are also files out there that can be both GIF and JS, both PPT and JS, etc.

GIFARs are possible because GIF images store their header in the beginning of the file, and JAR files (as with any ZIP archive-based format) store their data at the end. In this case, the JAR file is simply appended to the end of the GIF.

## Extra

Source Code: `f0vtW.java`<br>
JAR File: `app.jar`<br>
Original GIF: `giraffe wtf GIF.gif` from [Giphy](https://giphy.com/gifs/funny-wtf-ZkiIapyGO0u6Q)