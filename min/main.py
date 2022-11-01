from minio import Minio
from minio.error import S3Error


def main():

    client = Minio(
        "play.min.io",
        access_key="minioadmin",
        secret_key="minioadmin",
    )

    found = client.bucket_exists("bucket")
    if not found:
        client.make_bucket("bucket")
    else:
        print("Bucket 'bucket' already exists")

    client.fput_object(
        "bucket", "main.css", "./Cloud_web/min/main.css",
    )
    print(
        "'./main.css' is successfully uploaded as "
        "object 'main.css' to bucket 'bucket'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
