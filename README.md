# Self-Driving Car Simulation

A Flask-based autonomous driving simulation using TensorFlow/Keras for behavioral cloning. This project trains a neural network to predict steering angles from camera images, enabling autonomous driving in a simulated environment.

## Features

- **Data Processing**: Automated data balancing and augmentation
- **CNN Model**: NVIDIA-inspired architecture for steering angle prediction
- **Real-time Testing**: WebSocket-based server for simulation integration
- **Data Visualization**: Tools for analyzing training data distribution

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Docker Commands](#docker-commands)
6. [Project Structure](#project-structure)
7. [Model Architecture](#model-architecture)
8. [Data Format](#data-format)
9. [Troubleshooting](#troubleshooting)
10. [Team Best Practices](#team-best-practices)

---

## Quick Start

### For New Team Members

**Complete setup in 15 minutes:**

1. **Install Docker Desktop**
   - macOS: `brew install --cask docker`
   - Windows: [Download from docker.com](https://www.docker.com/products/docker-desktop/)
   - Linux: `curl -fsSL https://get.docker.com | sh`

2. **Clone and Build**
   ```bash
   git clone https://github.com/Kodekatt/MCFSD.git
   cd MCFSD
   docker-compose build
   ```

3. **Run the Server**
   ```bash
   docker-compose up
   ```
   Server runs on `http://localhost:4567`

   ⚠️ **Note:** The server requires a trained model. If you see "model.h5 not found", you need to train the model first (see [Training the Model](#training-the-model)).

### Checklist for New Developers

- [ ] Install Docker Desktop
- [ ] Clone repository
- [ ] Run `docker-compose build` (one-time, 5-10 min)
- [ ] Verify with `docker-compose up`
- [ ] Ready to work! 🎉

---

## Project Overview

This project uses Python 3.7 in a Docker container for consistent environment across all developers. The trained model predicts steering angles from camera frames in real-time.

### Key Components

- **trainingSimulation.py**: Trains the neural network model
- **testSimulation.py**: Inference server for real-time driving
- **utilis.py**: Data processing and model utilities

---

## Installation

### Prerequisites

- Docker Desktop installed
- ~5GB disk space for packages
- Training data in proper format (optional)

### First Time Setup

1. **Verify Docker Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Build the Container (one-time)**
   ```bash
   docker-compose build
   ```
   ⏱️ Takes 5-10 minutes on first run

3. **Verify Setup**
   ```bash
   docker-compose up
   ```
   You should see the server starting on port 4567. Press `Ctrl+C` to stop.

---

## Usage

### Training the Model

**Required:** Training data in `myData/` directory with:
- `driving_log.csv`
- `IMG/` folder with images

**Train the model:**
```bash
docker-compose run --rm fsd-simulation python trainingSimulation.py
```

The trained `model.h5` will be saved in the project directory.

### Running the Test Server

**Required:** A trained `model.h5` file

```bash
# Start the server
docker-compose up

# Server runs on http://localhost:4567
# Connect your simulator to this address
```

---

## Docker Commands

### Basic Commands

```bash
# Start server (detached mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop server
docker-compose down

# Rebuild container (if dependencies change)
docker-compose build
```

### Development Commands

```bash
# Run training
docker-compose run --rm fsd-simulation python trainingSimulation.py

# Access container shell
docker-compose exec fsd-simulation bash

# View running containers
docker-compose ps

# Interactive shell (fresh container)
docker-compose run --rm fsd-simulation bash
```

### Advanced Commands

```bash
# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up

# Use GPU (if available)
docker-compose run --rm --gpus all fsd-simulation python trainingSimulation.py
```

---

## Project Structure

```
.
├── trainingSimulation.py    # Model training script
├── testSimulation.py        # Model inference server
├── utilis.py                # Data processing utilities
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
├── .dockerignore            # Docker ignore rules
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── myData/                  # Training data directory
    ├── driving_log.csv
    └── IMG/
```

### Container Structure

```
/app/
├── myData/              # Training data (mounted from host)
│   ├── driving_log.csv
│   └── IMG/
├── model.h5            # Trained model (mounted from host)
├── trainingSimulation.py
├── testSimulation.py
└── utilis.py
```

---

## Model Architecture

The model uses a convolutional neural network inspired by NVIDIA's behavioral cloning approach:

- **5 convolutional layers** with increasing depth (24 → 36 → 48 → 64 → 64)
- **ELU activation functions** for smooth gradients
- **Fully connected layers** for regression (100 → 50 → 10 → 1)
- **Adam optimizer** with learning rate 0.001
- **MSE loss** for steering angle prediction

### Image Preprocessing

1. Crop to road region (60:135 pixels vertically)
2. Convert RGB to YUV color space
3. Apply Gaussian blur (3x3 kernel)
4. Resize to 200x66 (NVIDIA input size)
5. Normalize to [0, 1]

---

## Data Format

### CSV Format

The `driving_log.csv` should have these columns:

```csv
Center,Left,Right,Steering,Throttle,Brake,Speed
/path/to/image.jpg,/path/to/image.jpg,/path/to/image.jpg,0.0,1.0,0.0,30
```

### Directory Structure

```
myData/
├── driving_log.csv
└── IMG/
    ├── center_2021_01_01_12_00_00_000.jpg
    ├── left_2021_01_01_12_00_00_000.jpg
    └── right_2021_01_01_12_00_00_000.jpg
```

---

## Troubleshooting

### Common Issues

#### "Cannot connect to Docker daemon"
- **macOS/Windows:** Start Docker Desktop application
- **Linux:** Run `sudo systemctl start docker`

#### "Port 4567 is already in use"
```bash
# Stop existing container
docker-compose down

# Or change port in docker-compose.yml:
# ports: - "4568:4567"  # Use 4568 instead
```

#### "model.h5 not found"
This is normal on first run! You need to train first:
```bash
docker-compose run --rm fsd-simulation python trainingSimulation.py
```

#### Container needs rebuilding
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Permission Issues (Linux)
```bash
sudo docker-compose up
# Or add user to docker group:
sudo usermod -aG docker $USER
```

### Getting Help

1. Check Docker logs: `docker-compose logs -f`
2. View container status: `docker-compose ps`
3. Ask your team lead

---

## Team Best Practices

### Development Workflow

```bash
# Start working
git pull origin main

# If dependencies changed:
docker-compose build

# Start server (development)
docker-compose up

# Train model
docker-compose run --rm fsd-simulation python trainingSimulation.py

# Stop everything
docker-compose down
```

### Version Control

✅ **Do commit:**
- All code files (.py)
- requirements.txt
- Dockerfile, docker-compose.yml
- Documentation

❌ **Don't commit:**
- Container images
- Virtual environments (venv/)
- Cache files (__pycache__)
- Large data files (unless using Git LFS)
- .DS_Store files

### Sharing Data & Models

**Option 1: Git LFS (for small datasets)**
```bash
git lfs track "*.jpg"
git lfs track "model.h5"
```

**Option 2: Shared Network Drive**
Mount as volume in `docker-compose.yml`:
```yaml
volumes:
  - /path/to/shared/data:/app/myData:ro
```

**Option 3: Cloud Storage**
Mount S3/Dropbox as local volume

### Environment Variables

Add to `.env` file or `docker-compose.yml`:

```yaml
environment:
  - FLASK_DEBUG=1
  - TF_CPP_MIN_LOG_LEVEL=3
  - MODEL_PATH=/app/model.h5
  - DATA_PATH=/app/myData
```

---

## Advantages of Docker Setup

✅ **Python 3.7**: Matches original development environment  
✅ **No dependency conflicts**: All packages work together  
✅ **Isolated environment**: Won't affect your system Python  
✅ **Reproducible**: Same environment everywhere  
✅ **Easy cleanup**: Just remove the container  
✅ **Team consistency**: Everyone runs the same setup  

---

## License

This project is for educational purposes.

---

## Need Help?

- Check Docker logs: `docker-compose logs -f`
- View container status: `docker-compose ps`
- Access container shell: `docker-compose exec fsd-simulation bash`
- Ask your team lead
