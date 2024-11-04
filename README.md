# Hive Box Project [![Dynamic DevOps Roadmap](https://devopshive.net/badges/dynamic-devops-roadmap.svg)](https://github.com/DevOpsHiveHQ/dynamic-devops-roadmap)

Hive Box is a simple Flask application that utilizes [OpenSenseMap](https://opensensemap.org/) to retrieve weather data.

## Endpoints

This project is designed for learning DevOps fundamentals, so the application is very simple.

### Get Version

Returns the current version of the app.

You can use this [URL](http://a90310d6a02bd4e05b5d69102628ff7d-df5cbdbd151f860e.elb.eu-north-1.amazonaws.com/api/version) to access it, and the result should look like this:

```json
{
  "version": "v1"
}
```

### Get Average Temperature

Returns the average temperature collected by the box's sensors in the past hour.

You can use this [URL](http://a90310d6a02bd4e05b5d69102628ff7d-df5cbdbd151f860e.elb.eu-north-1.amazonaws.com/api/temperature) to access it, and the result should look like this:

```json
{
  "average_temperature": 13.472500000000002,
  "status": "Good"
}
```

It may feel slow the first time, this is why I used Cache to improve it.

### Get Metrics

Returns basic metrics about the app.

You can use this [URL](http://a90310d6a02bd4e05b5d69102628ff7d-df5cbdbd151f860e.elb.eu-north-1.amazonaws.com/api/metrics) to access it, and the result should look like this:

```
request_latency_seconds_bucket{endpoint="/api/temperature",le="10.0",method="GET"} 1.0
request_latency_seconds_bucket{endpoint="/api/temperature",le="+Inf",method="GET"} 1.0
request_latency_seconds_count{endpoint="/api/temperature",method="GET"} 1.0
request_latency_seconds_sum{endpoint="/api/temperature",method="GET"} 7.508691310882568
```

### Get Cache Status

Returns the status of the cache, indicating `ready` if the cache has data that is less than 5 minutes old. The caching is implemented using [Valkey](https://hub.docker.com/r/valkey/valkey/).

You can use this [URL](http://a90310d6a02bd4e05b5d69102628ff7d-df5cbdbd151f860e.elb.eu-north-1.amazonaws.com/api/readyz) to access it, and the result should look like this:

```json
{
  "ready": false,
  "reason": "Cache is empty :("
}
```

## DevOps Aspects

I have learned many concepts related to DevOps, which I will summarize briefly below.

### Docker

The Flask application is not deployed directly but as an image using Docker.

### Kubernetes

After the image is built and pushed to the GitHub registry, it is deployed as a pod using a Kubernetes cluster, which improves the application's scalability and reliability. Ingress is used to manage external access.

### AWS Hosting

I utilized an [AWS](https://aws.amazon.com/) free tier account to host the application, using the [EKS](https://aws.amazon.com/eks/) service for cluster management and the [S3](https://aws.amazon.com/s3/) service for storage.

### Continuous Integration

I used GitHub Actions to run various scans and tests on the code:

1. Running unit tests in an isolated environment.

2. Using [Scorecard](https://github.com/marketplace/actions/ossf-scorecard-action) for security evaluation.

3. Implementing [Terrascan](https://github.com/marketplace/actions/terrascan-iac-scanner) as a security best practices scanner.

4. Running linters: [PyLint](https://github.com/marketplace/actions/pylint-with-dynamic-badge) and [Hadolint](https://github.com/marketplace/actions/hadolint-action) for linting Python and Docker files.

#### Continuous Delivery

I used GitHub Actions to automate the deployment process, making it easier to deploy updates. Whenever a push or pull request occurs on the `main` branch, the following actions take place:

1. Build and push the image of Hive Box to the GitHub registry.

2. Sync Kubernetes manifest files from the repository to the S3 bucket.

3. Apply the new manifest files to the cluster.

4. Restart deployments using `Rollout`, ensuring that old deployments are preserved in case the new ones encounter issues.

In summary, whenever a new update is pushed to `main`, it is automatically deployed to the server.
