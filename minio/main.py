from minio import Minio
from minio.error import S3Error


def main():

    client = Minio(
        "play.min.io",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    )

    found = client.bucket_exists("minio")
    if not found:
        client.make_bucket("minio")
    else:
        print("Bucket 'minio' already exists")

    client.fput_object(
        "minio", "main.css", "./main.css",
    )
    print(
        "'./main.css' is successfully uploaded as "
        "object 'main.css' to bucket 'minio'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)