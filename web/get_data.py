from minio import Minio

client = Minio(
        "play.min.io",
        access_key="minioadmin",
        secret_key="minioadmin",
    )

r = client.get_object("bucket", "main.css")
data = r.read().decode("utf8")

filename = "./css/main.css"
with open(filename, "w") as f:
    f.write(data)

