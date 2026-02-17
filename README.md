## My Observations

### Rule Based Approach

For PDF Invoices, I ealrier opted for `PyMuPDF` and found that it's not layout aware, thus making the extraction miss some of the important info like Total Amount, Sub-Total etc. I did some research and found out a better aletrnative to this is `pdfplumber`. This gave better extraction with layout awareness. 

So far, With Heuristic approach I have observed there's no one-size fits all kind of logic we can write that is robuts enough to deal with different types of Invoices. Either I come up with logic and regex for all possible patterns or we move to intelligent systems for this. 