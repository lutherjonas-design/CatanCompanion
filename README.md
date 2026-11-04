# CatanCompanion

### ⚠️ **Project Status: Paused (Architectural Transition Study)**  
This project serves as a learning prototype for board game state tracking and initial API design. It was intentionally paused after discovering critical architectural constraints regarding real-time communication.

### 🛠️ **Tech Stack**
* **Backend:** Python, FastAPI
* **Frontend:** React

## Key Architectural Insights & Takeaways
* **The REST vs. WebSocket Dilemma:** The initial architecture relied on classic API routes (REST) for state synchronization. During development, it became evident that constant polling for a dynamic game board was highly inefficient and could lead to problems with 6 Players. 
* **The Pivot:** The project led to the crucial realization that a stateful game loop inherently requires **WebSockets** rather than stateless HTTP routes to manage component interaction effectively.
* **Frontend Coupling:** Working on the Catan Companion provided deep insights into data flow between a Python backend and a React component tree, forming the basis for my current modular architectures. The frontend is comparably empty, because with the realisation of needing a WebSocket it seemed unuseful for now
