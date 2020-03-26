# quip_reports

## Usage

**Output directory:** `/data/reports`

1. **Print images**

Prints a list of images for a given collection, with Collection, Study ID, Subject ID, Image ID, Date.  

For all collections, pass "all" instead of "collection name".
<!-- python3.6 images.py username password "collection name" -->

```
docker exec quip-reports images username password "collection name"
```

2. **Print annotations**

Prints list of images and their associated annotations, for a given collection.  Output columns: Collection, Study ID, Subject ID, Image ID, Analysis type, Execution ID, Creator, Date.

<!-- For all collections, pass "all" instead of "collection name". -->
<!-- python3.6 annotations.py username password "collection name" -->

```
docker exec quip-reports annotations username password "collection name"
```

<!-- 
docker build -t quip_reports . && docker run --network="quip_distro_default" --name quip-reports -it -d quip_reports /bin/bash
-->
