# Project Flow

```mermaid
flowchart TD
A[Project Manager] --> B[Dashboard]
B --> C[FastAPI]
C --> D[(Projects and Activities)]
D --> E[Progress Aggregation]
D --> F[Delay Risk Model]
F --> B
E --> B
```
