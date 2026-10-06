# Scaling to 100 concurrent users

For this assignment prototype, a single local Uvicorn process and SQLite are enough. For roughly 100 simultaneous users, I would:

1. Load the model once per worker instead of per request.
2. Run multiple Uvicorn workers behind a reverse proxy/load balancer.
3. Move SQLite to PostgreSQL if concurrent writes become a bottleneck.
4. Add request timeouts, rate limiting, structured logs and health checks.
5. Keep the prediction endpoint stateless apart from a short database write.
6. Monitor latency, error rate and database contention.
7. Containerize the service and use horizontal replicas.
